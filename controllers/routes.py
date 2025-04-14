from flask import render_template, request, redirect, url_for, flash
from models.database import db, Veiculo, Imagem
import os
import uuid


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

   # @app.route('/estoque')
   # def estoque():
    #    veiculosestoque = Veiculo.query.all()
     #   return render_template('estoque.html', veiculosestoque=veiculosestoque)
    
    # CRUD - listagem e cadastro
    @app.route('/estoque' ,methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            veiculo = Veiculo.query.get(id)
            # Deleta o cadastro pela ID
            db.session.delete(veiculo)
            db.session.commit()
            return redirect(url_for('estoque'))
        #Cadastra novo veiculo
        if request.method == 'POST':
            newveiculo = Veiculo(
                request.form['marca'], 
                request.form['modelo'], 
                request.form['ano'], 
                request.form['cor'], 
                request.form['combustivel'], 
                request.form['preco'], 
                request.form['estoque'],
            )
            db.session.add(newveiculo)
            db.session.commit()
            return redirect(url_for('estoque'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 5
            veiculos_page = Veiculo.query.paginate(page=page, per_page=per_page) 
            return render_template('estoque.html', veiculosestoque=veiculos_page)

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        v = Veiculo.query.get(id)
        # Edita o cadastro do veiculo com as informações do formulário
        if request.method == 'POST':
            v.marca = request.form['marca']
            v.modelo = request.form['modelo']
            v.ano = request.form['ano']
            v.cor = request.form['cor']
            v.combustivel = request.form['combustivel']
            v.preco = request.form['preco']
            v.estoque = request.form['estoque']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editarveiculo.html', v=v)

    #Definindo os tipos de arquivos permitidos
    FILE_TYPES = set(['png','jpg','jpeg','gif',])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES

    # Upload de imagens
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagens = Imagem.query.all()  # Carrega as imagens para ambos GET e POST
    
        if request.method == 'POST':
            # Verifica se o arquivo foi enviado
            if 'file' not in request.files:
                flash('Nenhum arquivo selecionado', 'danger')
                return redirect(request.url)
                
            file = request.files['file']
            
            # Verifica se um arquivo foi selecionado
            if file.filename == '':
                flash('Nenhum arquivo selecionado', 'danger')
                return redirect(request.url)
                
            # Verifica a extensão do arquivo
            if file and arquivos_permitidos(file.filename):
                # Gera um nome único mantendo a extensão original
                file_ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4()}{file_ext}"
                
                # Salva no banco de dados
                img = Imagem(filename=filename)
                db.session.add(img)
                db.session.commit()
                
                # Salva o arquivo fisicamente
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                flash("Imagem enviada com sucesso!", 'success')
                return redirect(url_for('galeria'))  # Redireciona para GET
                
            else:
                flash("Apenas arquivos PNG, JPG, JPEG ou GIF são permitidos", 'danger')
        
        return render_template('galeria.html', imagens=imagens)

    



