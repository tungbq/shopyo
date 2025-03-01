import json
import os

from flask import current_app
from flask import flash
from flask import render_template
from flask_login import login_required
from modules.box__default.appadmin.admin import admin_required
from modules.box__default.auth.decorators import check_confirmed

from shopyo.api.html import notify_success
from shopyo.api.module import ModuleHelp

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


all_info = {}


@dashboard_blueprint.route("/")
@login_required
@check_confirmed
@admin_required
def index():
    context = {}

    for folder in os.listdir(os.path.join(current_app.config["BASE_DIR"], "modules")):
        if folder.startswith("__"):
            continue
        elif folder.startswith("box__"):
            for sub_folder in os.listdir(
                os.path.join(current_app.config["BASE_DIR"], "modules", folder)
            ):
                if sub_folder in ["dashboard"]:
                    continue
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                with open(
                    os.path.join(
                        current_app.config["BASE_DIR"],
                        "modules",
                        folder,
                        sub_folder,
                        "info.json",
                    )
                ) as f:
                    module_info = json.load(f)
                    all_info[sub_folder] = module_info
        else:
            if folder not in ["dashboard"]:
                with open(
                    os.path.join(
                        current_app.config["BASE_DIR"],
                        "modules",
                        folder,
                        "info.json",
                    )
                ) as f:
                    module_info = json.load(f)
                    all_info[folder] = module_info

    context["all_info"] = all_info
    flash(notify_success("Notif test"))
    return render_template("dashboard/index.html", **context)
