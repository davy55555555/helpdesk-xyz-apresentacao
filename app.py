"""Protótipo local: dados fictícios, sem autenticação real ou persistência."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from html import escape
from datetime import datetime
from threading import Lock

lock = Lock()
chamados = []
perfis = {'cliente': 'Cliente', 'tecnico': 'Técnico', 'administrador': 'Administrador'}

def page(perfil, aviso=''):
    rows = []
    for c in chamados:
        if perfil == 'tecnico' and not c['atribuido']:
            continue
        comments = ''.join('<li>' + escape(x) + '</li>' for x in c['comentarios']) or '<li>Nenhum comentário</li>'
        actions = ''
        if perfil == 'administrador' and c['status'] == 'Pendente':
            actions += button(c['id'], perfil, 'atribuir', 'Atribuir ao técnico')
        if perfil == 'tecnico' and c['status'] == 'Em andamento':
            actions += form(c['id'], perfil, 'resolver', '<input name="solucao" placeholder="Solução" required>', 'Resolver')
        if perfil == 'cliente' and c['status'] in ('Pendente', 'Em andamento'):
            actions += button(c['id'], perfil, 'cancelar', 'Cancelar chamado')
        if perfil in ('cliente', 'tecnico') and c['status'] in ('Pendente', 'Em andamento'):
            actions += form(c['id'], perfil, 'comentar', '<input name="texto" placeholder="Comentário" required>', 'Comentar')
        rows.append('<article><h3>#{id:03} — {titulo}</h3><p>{desc}</p><p>Prioridade: {prioridade} | Situação: {status} | Técnico: {tecnico}</p><p>Solução: {solucao}</p><ul>{comments}</ul>{actions}</article>'.format(id=c['id'], titulo=escape(c['titulo']), desc=escape(c['descricao']), prioridade=escape(c['prioridade']), status=escape(c['status']), tecnico='Técnico de teste' if c['atribuido'] else 'Não atribuído', solucao=escape(c['solucao'] or 'Não registrada'), comments=comments, actions=actions))
    create = ''
    if perfil == 'cliente':
        create = '''<h2>Abrir chamado</h2><form method="post"><input type="hidden" name="perfil" value="cliente"><input type="hidden" name="acao" value="abrir"><label>Título <input name="titulo" maxlength="120" required></label><label>Descrição <textarea name="descricao" maxlength="2000" required></textarea></label><label>Prioridade <select name="prioridade"><option>Baixa</option><option selected>Média</option><option>Alta</option></select></label><button>Abrir chamado</button></form>'''
    options = ''.join(f'<option value="{k}" {"selected" if k==perfil else ""}>{v}</option>' for k,v in perfis.items())
    return f'''<!doctype html><html lang="pt-br"><meta charset="utf-8"><title>HelpDesk XYZ — protótipo</title><style>body{{font:16px Arial;max-width:900px;margin:30px auto;padding:0 20px;color:#203046}}h1{{color:#123760}}article{{border:1px solid #b8c6d5;border-radius:6px;padding:14px;margin:14px 0}}label{{display:block;margin:12px 0}}input,textarea,select,button{{font:inherit;padding:8px}}textarea{{display:block;width:90%}}button{{cursor:pointer}}form.inline{{display:inline-block;margin:4px}}</style><h1>HelpDesk XYZ</h1><p><strong>Protótipo local com dados fictícios.</strong> A troca de perfil simula autenticação; os dados são apagados ao encerrar o programa.</p><form method="get"><label>Perfil de demonstração <select name="perfil">{options}</select> <button>Trocar perfil</button></label></form><p>{escape(aviso)}</p>{create}<h2>Chamados</h2>{''.join(rows) or '<p>Nenhum chamado disponível para este perfil.</p>'}<p>Anexos e autenticação real não estão implementados.</p></html>'''

def form(cid, perfil, acao, fields, label):
    return f'<form class="inline" method="post"><input type="hidden" name="id" value="{cid}"><input type="hidden" name="perfil" value="{perfil}"><input type="hidden" name="acao" value="{acao}">{fields}<button>{label}</button></form>'
def button(cid, perfil, acao, label): return form(cid, perfil, acao, '', label)

def transition(data):
    perfil=data.get('perfil','cliente'); acao=data.get('acao','');
    if perfil not in perfis: return 'cliente', 'Perfil inválido.'
    if acao=='abrir' and perfil=='cliente':
        titulo=data.get('titulo','').strip(); desc=data.get('descricao','').strip(); prioridade=data.get('prioridade','')
        if not titulo or not desc or len(titulo)>120 or len(desc)>2000 or prioridade not in ('Baixa','Média','Alta'): return perfil,'Dados inválidos.'
        c={'id':len(chamados)+1,'titulo':titulo,'descricao':desc,'prioridade':prioridade,'status':'Pendente','atribuido':False,'solucao':'','comentarios':[],'abertura':datetime.now().isoformat()};chamados.append(c);return perfil,f'Chamado criado. Protocolo: {c["id"]:03}.'
    try: c=next(x for x in chamados if x['id']==int(data.get('id','')))
    except (ValueError,StopIteration): return perfil,'Chamado não encontrado.'
    if acao=='atribuir' and perfil=='administrador' and c['status']=='Pendente': c['atribuido']=True;c['status']='Em andamento';return perfil,'Chamado atribuído.'
    if acao=='resolver' and perfil=='tecnico' and c['atribuido'] and c['status']=='Em andamento':
        sol=data.get('solucao','').strip()
        if not sol or len(sol)>2000:return perfil,'Informe uma solução válida.'
        c['solucao']=sol;c['status']='Resolvido';return perfil,'Chamado resolvido.'
    if acao=='cancelar' and perfil=='cliente' and c['status'] in ('Pendente','Em andamento'):c['status']='Cancelado';return perfil,'Chamado cancelado.'
    if acao=='comentar' and perfil in ('cliente','tecnico') and c['status'] in ('Pendente','Em andamento') and (perfil!='tecnico' or c['atribuido']):
        text=data.get('texto','').strip()
        if not text or len(text)>2000:return perfil,'Informe um comentário válido.'
        c['comentarios'].append(perfis[perfil]+': '+text);return perfil,'Comentário registrado.'
    return perfil,'Operação não permitida para este perfil ou estado.'

class Handler(BaseHTTPRequestHandler):
    def respond(self,perfil,msg=''):
        with lock: body=page(perfil,msg).encode('utf-8')
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        p=parse_qs(self.path.partition('?')[2]).get('perfil',['cliente'])[0];self.respond(p if p in perfis else 'cliente')
    def do_POST(self):
        try: length=int(self.headers.get('Content-Length','0'))
        except ValueError: self.send_error(400);return
        if length<=0 or length>16384:self.send_error(400);return
        raw=parse_qs(self.rfile.read(length).decode('utf-8'),keep_blank_values=True);data={k:v[0] for k,v in raw.items()}
        with lock: perfil,msg=transition(data)
        self.respond(perfil,msg)
    def log_message(self,*args): pass

if __name__=='__main__':
    print('Acesse http://127.0.0.1:8501 — Ctrl+C para encerrar.', flush=True)
    ThreadingHTTPServer(('127.0.0.1',8501),Handler).serve_forever()
