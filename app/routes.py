from datetime import date

from flask import Blueprint, Response, current_app, render_template, request

pages = Blueprint("pages", __name__)

PAGE_META = {
    "home": (
        "Programa para hacer tickets de venta gratis | FácilTicket",
        "Crea productos, registra tus ventas e imprime tickets con FácilTicket. Un programa sencillo para pequeños negocios. Empieza gratis.",
    ),
    "funcionalidades": (
        "Funciones para crear e imprimir tickets | FácilTicket",
        "Descubre las funciones de FácilTicket para preparar productos, registrar ventas y crear tickets de una forma sencilla.",
    ),
    "como-funciona": (
        "Cómo funciona FácilTicket: crea e imprime tus tickets",
        "Descubre cómo preparar tus productos, registrar una venta y crear un ticket con FácilTicket en unos pasos sencillos.",
    ),
    "preguntas-frecuentes": (
        "Preguntas frecuentes sobre FácilTicket",
        "Resuelve tus dudas sobre el funcionamiento, la versión gratuita, el registro de ventas y la impresión de tickets con FácilTicket.",
    ),
    "blog": (
        "Blog sobre tickets de venta y TPV sencillo | FácilTicket",
        "Guías sencillas sobre tickets de venta, impresión, factura simplificada, TPV y gestión básica para pequeños negocios.",
    ),
    "contacto": (
        "Contacto | FácilTicket",
        "Contacta con FácilTicket para resolver dudas sobre el programa y su funcionamiento.",
    ),
}


def page_context(page, path, **extra):
    title, description = PAGE_META.get(
        page,
        (f"{extra.get('heading', page)} | FácilTicket", "Información de FácilTicket."),
    )
    base = current_app.config["PUBLIC_BASE_URL"]
    return {
        "page": page,
        "title": title,
        "description": description,
        "canonical": f"{base}{path}",
        "registration_url": current_app.config["REGISTRATION_URL"],
        "login_url": current_app.config["LOGIN_URL"],
        "contact_email": current_app.config["CONTACT_EMAIL"],
        "current_year": date.today().year,
        **extra,
    }


@pages.get("/")
def home():
    return render_template("home.html", **page_context("home", "/"))


@pages.get("/funcionalidades/")
def funcionalidades():
    return render_template(
        "funcionalidades.html", **page_context("funcionalidades", "/funcionalidades/")
    )


@pages.get("/como-funciona/")
def como_funciona():
    return render_template(
        "como-funciona.html", **page_context("como-funciona", "/como-funciona/")
    )


@pages.get("/preguntas-frecuentes/")
def preguntas_frecuentes():
    return render_template(
        "preguntas-frecuentes.html",
        **page_context("preguntas-frecuentes", "/preguntas-frecuentes/"),
    )


@pages.get("/blog/")
def blog():
    return render_template("blog.html", **page_context("blog", "/blog/"))


@pages.get("/contacto/")
def contacto():
    return render_template("contacto.html", **page_context("contacto", "/contacto/"))


@pages.get("/<page_name>/")
def legal(page_name):
    legal_pages = {
        "aviso-legal": "Aviso legal",
        "privacidad": "Política de privacidad",
        "cookies": "Política de cookies",
        "terminos": "Términos de uso",
    }
    if page_name not in legal_pages:
        return not_found(None)
    heading = legal_pages[page_name]
    template = "aviso-legal.html" if page_name == "aviso-legal" else "legal.html"
    return render_template(
        template, **page_context(page_name, f"/{page_name}/", heading=heading)
    )


@pages.get("/robots.txt")
def robots():
    base = current_app.config["PUBLIC_BASE_URL"]
    body = f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@pages.get("/sitemap.xml")
def sitemap():
    base = current_app.config["PUBLIC_BASE_URL"]
    paths = [
        "/", "/funcionalidades/", "/como-funciona/", "/preguntas-frecuentes/",
        "/blog/", "/contacto/", "/aviso-legal/", "/privacidad/", "/cookies/",
        "/terminos/",
    ]
    urls = "".join(f"<url><loc>{base}{path}</loc></url>" for path in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, mimetype="application/xml")


@pages.get("/health")
def health():
    return {"status": "ok"}


@pages.app_errorhandler(404)
def not_found(error):
    context = page_context("404", request.path, heading="Página no encontrada")
    context["robots"] = "noindex, follow"
    return render_template("404.html", **context), 404
