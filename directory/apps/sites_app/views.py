from . import sites
from directory.utils.request import json_only


@sites.route('/', methods=['POST'])
@json_only
def create_site():
    pass
