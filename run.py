from app.resources.base import Index
from app.resources.auth import UserLogin, UserRegister
from app.resources.bucketlists import BucketListsAPI, BucketListAPI
from app.resources.items import ItemsAPI, ItemAPI
from app import api, app

""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(UserRegister, "/auth/register/")
api.add_resource(UserLogin, "/auth/login/")
api.add_resource(BucketListsAPI, "/bucketlists/")
api.add_resource(BucketListAPI, "/bucketlists/<id>")
api.add_resource(ItemsAPI, "/bucketlists/<id>/items/")
api.add_resource(ItemAPI, "/bucketlists/<id>/items/<item_id>")

if __name__ == "__main__":
    app.run()
