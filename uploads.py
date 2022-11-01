from flask_uploads import IMAGES, UploadSet, DOCUMENTS

gift_images = UploadSet('gifts', IMAGES)
achievement_files = UploadSet('achievementfiles', DOCUMENTS + IMAGES)
