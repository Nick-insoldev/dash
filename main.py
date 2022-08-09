from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from src.layout import create_layout
from dash_extensions.enrich import DashProxy, MultiplexerTransform
def main() -> None:
    # app = Dash(external_stylesheets=[BOOTSTRAP])
    app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[BOOTSTRAP])
    app.title = "Insoldev bv Raport tool"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()