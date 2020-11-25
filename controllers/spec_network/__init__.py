from flask import Blueprint

mod = Blueprint('spec_network', __name__,
                template_folder='templates', url_prefix='/')
from . import routes, events
