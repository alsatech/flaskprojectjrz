from .. import mailsender, db
from flask import current_app, render_template, Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.models import UsuarioModel, ProductModel
from main.auth.decorators import role_required


def send_mail(to, subject, template, **kwargs):
    
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'])
    try:

        msg.body =  render_template(f'{template}.txt', **kwargs)
        mailsender.send(msg)
    
    except SMTPException as error:
        return 'Mail deliver failed'
    return True

mail = Blueprint('mail', __name__, url_prefix='/mail')

@mail.route('/newsletter', methods=['POST'])
@role_required(roles=["admin"])
def newsletter():
    usuarios = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente').all
    ()
    productos = db.session.query(ProductModel).all()
    try:
        for usuario in usuarios:
            send_mail([usuario.email], "Productos en Venta", 'newsletter', usuario =
            usuario, productos = [producto.nombre for producto in productos])
    except SMTPException as error:
        return 'Mail deliver failed'
    return 'mails sent', 200
