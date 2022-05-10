from flask_uploads import IMAGES, UploadSet

avatars = UploadSet('avatars', IMAGES)
gift_images = UploadSet('gifts', IMAGES)
