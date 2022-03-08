from cmath import log
from flask_app import app
from flask import render_template, redirect, session, request, jsonify
from flask_app.config.helper_func import checkLogin

from flask_app.models import model_post, model_category, model_page

@app.route('/posts')  
@checkLogin        
def post_new():
    session['page'] = 'Posts'
    context = {
        'all_posts': model_post.Post.get_all(),
        'all_categories': model_category.Category.get_all()
    }
    return render_template('admin/post.html', **context)

@app.route('/post/create', methods=['POST'])      
@checkLogin    
def post_create():
    id = model_post.Post.create(**request.form, user_id=session['uuid'])
    return redirect(f'/post/{id}/edit')

@app.route('/post/<int:id>')  
@checkLogin        
def post_show(id):
    context = {
        'post': model_post.Post.get_one(id=id),
    }
    return render_template('main/post_show.html', **context)

@app.route('/post/<int:id>/edit') 
@checkLogin         
def post_edit(id):
    session['page'] = 'Edit Post'
    context = {
        'post': model_post.Post.get_one(id=id),
        'all_categories': model_category.Category.get_all()
    }
    return render_template('admin/post_edit.html', **context)

@app.route('/post/<int:id>/update', methods=['POST'])   
@checkLogin       
def post_update(id):
    data ={**request.form}
    del data['files']

    if 'is_public' in request.form:
        data['is_public'] = 1
    else:
        data['is_public'] = 0


    if 'is_featured' in request.form:
        data['is_featured'] = 1
    else:
        data['is_featured'] = 0


    model_post.Post.update_one(**data, id=id)
    return redirect(f'/post/{id}/edit')

@app.route('/api/post/<int:id>/update', methods=['POST'])    
@checkLogin      
def api_post_update(id):
    data ={**request.form}
    model_post.Post.update_one(**data, id=id)
    return jsonify(msg='success')

@app.route('/post/<int:id>/delete')          
@checkLogin
def post_delete(id):
    model_post.Post.delete_one(id=id)
    return redirect('/posts')
