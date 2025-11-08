# 🚀 Guia de Deploy - GitHub Pages

Este guia explica como fazer o deploy do site do curso no GitHub Pages.

## 📋 Pré-requisitos

1. Conta no GitHub
2. Git instalado localmente
3. Repositório criado no GitHub

## 🔧 Configuração Inicial

### 1. Criar Repositório no GitHub

1. Vá para [github.com](https://github.com)
2. Clique em "New Repository"
3. Nome sugerido: `robot` ou `robotica-curso`
4. Marque como **Public**
5. Clique em "Create repository"

### 2. Inicializar Git Localmente

```bash
cd C:\Users\neima\projetosCC\robo

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "🎉 Inicial commit - Curso completo de Robótica"

# Adicionar remote
git remote add origin https://github.com/inematds/robot.git

# Push para GitHub
git push -u origin master
```

## ⚙️ Configurar GitHub Pages

### Opção A: Via GitHub Actions (Recomendado)

O arquivo `.github/workflows/pages.yml` já está configurado!

1. Vá para o repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Pages**
4. Em **Source**, selecione:
   - **GitHub Actions**
5. Clique em **Save**

O deploy será automático a cada push na branch `main`!

### Opção B: Deploy Manual

1. Vá para **Settings** > **Pages**
2. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/docs`
3. Clique em **Save**

## 🌐 Acessar o Site

Após alguns minutos, seu site estará disponível em:

```
https://inematds.github.io/robot/
```

✅ **Seu site está publicado em:** https://inematds.github.io/robot/

## 🔄 Atualizando o Site

Sempre que você fizer mudanças:

```bash
# Adicionar arquivos modificados
git add .

# Commit com mensagem descritiva
git commit -m "✨ Adiciona novos recursos X"

# Enviar para GitHub
git push
```

O GitHub Pages atualiza automaticamente em 1-2 minutos!

## 🎨 Personalização

### Mudar o Nome do Repositório

Se você quiser mudar o nome do repo depois:

1. **Settings** > **General** > **Repository name**
2. Digite o novo nome
3. Clique em **Rename**

A URL mudará para: `https://inematds.github.io/NOVO-NOME/`

### Custom Domain (Opcional)

Se você tem um domínio próprio:

1. Adicione um arquivo `CNAME` na pasta `docs/`:
   ```
   robotica.seudominio.com
   ```
2. Configure o DNS do domínio apontando para:
   ```
   inematds.github.io
   ```

## 📊 Monitorar Deploys

1. Vá para a aba **Actions** no repositório
2. Veja o status dos deployments
3. Clique em qualquer workflow para ver detalhes

## 🐛 Troubleshooting

### Site não carrega

- ✅ Verifique se o repositório é **Public**
- ✅ Confirme que GitHub Pages está ativado em Settings
- ✅ Aguarde 5-10 minutos após o primeiro deploy

### CSS/JS não carregam

- ✅ Verifique que o arquivo `.nojekyll` existe em `docs/`
- ✅ Confirme que os caminhos em `index.html` são relativos

### 404 Error

- ✅ Certifique-se de que o arquivo `index.html` está em `docs/`
- ✅ Verifique a branch configurada no Pages

### Workflow falhando

- ✅ Vá em Settings > Actions > General
- ✅ Em "Workflow permissions", selecione "Read and write permissions"
- ✅ Marque "Allow GitHub Actions to create and approve pull requests"

## 📝 Estrutura de Arquivos

```
robot/
├── docs/                   # ← Pasta servida pelo GitHub Pages
│   ├── .nojekyll          # ← Importante!
│   ├── index.html         # ← Página inicial
│   ├── materiais.html
│   ├── recursos.html
│   ├── instrutor.html
│   ├── nivel1.html
│   ├── nivel2.html
│   ├── nivel3.html
│   ├── css/
│   ├── js/
│   └── imagens/
├── .github/
│   └── workflows/
│       └── pages.yml      # ← GitHub Actions config
├── README.md
└── DEPLOY.md              # ← Este arquivo
```

## 🎯 Checklist de Deploy

- [ ] Repositório criado no GitHub
- [ ] Git inicializado localmente
- [ ] Arquivos commitados
- [ ] Push para origin/main
- [ ] GitHub Pages ativado
- [ ] Arquivo `.nojekyll` presente em `docs/`
- [ ] Aguardar 5-10 minutos
- [ ] Acessar URL e testar

## 🔗 Links Úteis

- [Documentação GitHub Pages](https://docs.github.com/pages)
- [GitHub Actions](https://docs.github.com/actions)
- [Troubleshooting](https://docs.github.com/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites)

## 💡 Dicas

1. **Sempre teste localmente** antes de fazer push
2. **Commits frequentes** com mensagens claras
3. **Use branches** para features maiores
4. **Revise** o site após cada deploy

---

🤖 **Boa sorte com seu projeto!**

Para dúvidas, abra uma [Issue no repositório](https://github.com/inematds/robot/issues).
