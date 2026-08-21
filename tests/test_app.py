from app import create_app


def client():
    app = create_app({"TESTING": True, "PUBLIC_BASE_URL": "https://facilticket.es"})
    return app.test_client()


def test_public_routes():
    paths = ["/", "/funcionalidades/", "/como-funciona/", "/preguntas-frecuentes/", "/blog/", "/contacto/", "/aviso-legal/", "/privacidad/", "/cookies/", "/terminos/", "/robots.txt", "/sitemap.xml", "/health"]
    for path in paths:
        assert client().get(path).status_code == 200


def test_not_found_is_real_404():
    response = client().get("/no-existe/")
    assert response.status_code == 404
    assert b"noindex, follow" in response.data


def test_home_seo_and_registration_link():
    response = client().get("/")
    assert b"Programa para hacer tickets de venta gratis" in response.data
    assert b"https://app.facilticket.es/registro" in response.data
    assert b'<link rel="canonical" href="https://facilticket.es/">' in response.data


def test_sitemap_contains_only_marketing_domain():
    response = client().get("/sitemap.xml")
    assert b"https://facilticket.es/funcionalidades/" in response.data
    assert b"app.facilticket.es" not in response.data


def test_legal_notice_contains_approved_owner_details():
    response = client().get("/aviso-legal/")
    assert response.status_code == 200
    assert b"Global Vendalia SLU" in response.data
    assert b"B67210443" in response.data
    assert b"info@ticketfacil.es" in response.data
