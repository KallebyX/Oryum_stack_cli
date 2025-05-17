from flask import request, flash, redirect, url_for, render_template
from models.usuario import Usuario
from models.base import db
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid

class UsuarioController:
    def index():
        """Lista todos os usuários."""
        usuarios = Usuario.query.all()
        return render_template('usuario/index.html', usuarios=usuarios)
    
    def create():
        """Exibe formulário para criar usuário."""
        usuario = Usuario()
        return render_template('usuario/create.html', usuario=usuario)
    
    def store():
        """Salva novo usuário no banco de dados."""
        try:
            usuario = Usuario()
            usuario.nome = request.form.get('nome')
            usuario.email = request.form.get('email')
            usuario.senha = request.form.get('senha')
            usuario.perfil = request.form.get('perfil', 'usuario')
            
            # Upload de foto
            if 'foto_perfil' in request.files and request.files['foto_perfil'].filename:
                arquivo = request.files['foto_perfil']
                filename = secure_filename(f"{uuid.uuid4()}_{arquivo.filename}")
                filepath = os.path.join('static/uploads/perfil', filename)
                
                # Salvar arquivo
                arquivo.save(filepath)
                
                # Processar imagem
                with Image.open(filepath) as img:
                    img = img.resize((200, 200))
                    img.save(filepath, optimize=True, quality=85)
                
                usuario.foto_perfil = filepath
            
            # Salvar no banco
            db.session.add(usuario)
            db.session.commit()
            
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('usuario.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar usuário: {str(e)}', 'danger')
            return render_template('usuario/create.html', usuario=usuario)
    
    def show(id):
        """Exibe detalhes de um usuário."""
        usuario = Usuario.query.get_or_404(id)
        return render_template('usuario/show.html', usuario=usuario)
    
    def edit(id):
        """Exibe formulário para editar usuário."""
        usuario = Usuario.query.get_or_404(id)
        return render_template('usuario/edit.html', usuario=usuario)
    
    def update(id):
        """Atualiza usuário no banco de dados."""
        usuario = Usuario.query.get_or_404(id)
        
        try:
            usuario.nome = request.form.get('nome')
            usuario.email = request.form.get('email')
            
            if request.form.get('senha'):
                usuario.senha = request.form.get('senha')
                
            usuario.perfil = request.form.get('perfil', usuario.perfil)
            
            # Upload de foto
            if 'foto_perfil' in request.files and request.files['foto_perfil'].filename:
                arquivo = request.files['foto_perfil']
                filename = secure_filename(f"{uuid.uuid4()}_{arquivo.filename}")
                filepath = os.path.join('static/uploads/perfil', filename)
                
                # Salvar arquivo
                arquivo.save(filepath)
                
                # Processar imagem
                with Image.open(filepath) as img:
                    img = img.resize((200, 200))
                    img.save(filepath, optimize=True, quality=85)
                
                # Remover foto antiga se existir
                if usuario.foto_perfil and os.path.exists(usuario.foto_perfil):
                    os.remove(usuario.foto_perfil)
                    
                usuario.foto_perfil = filepath
            
            # Salvar no banco
            db.session.commit()
            
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('usuario.show', id=usuario.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
            return render_template('usuario/edit.html', usuario=usuario)
    
    def destroy(id):
        """Remove usuário do banco de dados."""
        usuario = Usuario.query.get_or_404(id)
        
        try:
            # Remover foto se existir
            if usuario.foto_perfil and os.path.exists(usuario.foto_perfil):
                os.remove(usuario.foto_perfil)
                
            db.session.delete(usuario)
            db.session.commit()
            
            flash('Usuário removido com sucesso!', 'success')
            return redirect(url_for('usuario.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover usuário: {str(e)}', 'danger')
            return redirect(url_for('usuario.show', id=usuario.id))
