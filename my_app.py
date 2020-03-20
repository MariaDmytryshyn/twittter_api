from flask import Flask, render_template


app = Flask(_name_)


@app.route("/")
def prod():
    return render_template("My_world_map_with_friends_locations.html")


if _name_ == "_main_":
    app.run(debug = True)