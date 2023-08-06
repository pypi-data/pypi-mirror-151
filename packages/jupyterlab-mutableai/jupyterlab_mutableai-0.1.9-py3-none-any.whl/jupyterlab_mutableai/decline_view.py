import json
import os
import tornado
import shutil

from jupyter_server.base.handlers import APIHandler


def decline_changes(dirname, uid):
    """
    Delete the unique folder name if declined.
    """
    if not uid:
        return False
    dirpath = os.path.join(dirname, "." + uid)

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        return True
    return False


class DeclineRouterHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jlab-ext-example/TRANSFORM_NB endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()

        dirname = input_data["dirname"]
        uid = input_data["uid"]

        status = decline_changes(dirname, uid)

        if status:
            self.finish({"status": "completed"})
        else:
            self.finish({"status": "failed"})
