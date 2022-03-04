import os
from datetime import datetime

from flask import abort, flash, redirect, render_template, request, url_for, make_response

from app import app, db
from cv6Zadani.db import Centers, Reservation
from cv6Zadani.geo import get_location, get_map_image

IMAGE_DIR = os.path.abspath("images")


@app.route("/", methods=["GET"])
def index():
    center = db.session.query(Centers).all()
    return render_template("index.html", centers=center)


@app.route("/center", methods=["POST"])
def add_center():
    # TODO: add center to database
    form = request.form
    misto = form.get("location")
    gps = get_location(misto)
    if misto is None or len(misto.strip()) < 2 or len(misto.strip()) > 40:
        flash("Nezadano zadne mesto!!", "error")
        return redirect(url_for("index"))

    center = Centers(name=misto, lat=gps.lat, lon=gps.lon)

    db.session.add(center)
    db.session.commit()
    return redirect(url_for("index"))
    pass


@app.route("/center/<int:id>", methods=["GET"])
def center(id: int):
    # TODO: render templates/vaccinaton-center.html
    center = db.session.query(Centers).get(id)
    if not center:
        abort(404)
    return render_template("vaccination-center.html", center=center)



@app.route("/center/<int:id>/image", methods=["GET"])
def center_map(id: int):
    # TODO: return map JPG image as bytes
    center = db.session.query(Centers).get(id)
    image = get_map_image(center.name)
    if not center:
        abort(404)
    return image
    with open(center.image, "rb") as f:
        f.read()
    pass


@app.route("/center/<int:id>/reservation", methods=["POST"])
def reservation_add(id: int):
    # TODO: add reservation
    center = db.session.query(Centers).get(id)
    #reservations = request.form
    name = request.form.get("name")
    date = request.form.get("date")

    if name is None or len(name.strip()) < 2 or len(name.strip()) > 40 or date is None or not date.strip()\
            or len(date) > 100:
        flash("Zadny vstup!", "error")
        return redirect(url_for("center",id=id))

    date = datetime.strptime(date, "%Y-%m-%d")
    reservation = Reservation(name=name, date=date, center=center)
    center.reservations.append(reservation)
    db.session.commit()

    flash("rezervace pridana")
    return redirect(url_for("center", id=id))
    pass



@app.route("/center/<int:center_id>/reservation/<int:id>", methods=["POST"])
def reservation_delete(center_id: int, id: int):
    # TODO: delete reservation
    center = db.session.query(Reservation).get(id)
    db.session.delete(center)
    db.session.commit()

    flash("rezervace smazana!")
    return redirect(url_for("center",id=center_id))
    pass


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
