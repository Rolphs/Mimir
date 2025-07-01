from __future__ import annotations

"""Engine for translating symbolic profiles into design code snippets."""

from typing import Dict, Union

from .models import SymbolicProfile
from .mappings import generate_styles


class TranslationLayer:
    """Convert design variables into CSS and React code snippets."""

    def to_css(self, styles: Dict[str, str]) -> str:
        """Return a minimal CSS snippet applying the styles."""
        color = styles.get("color_primario", "#FFF")
        font = styles.get("fuente_base", "sans-serif")
        return (
            ".profile {\n"
            f"  color: {color};\n"
            f"  font-family: {font};\n"
            "}"
        )

    def to_react(self, styles: Dict[str, str]) -> str:
        """Return a React component snippet using the styles."""
        color = styles.get("color_primario", "#FFF")
        font = styles.get("fuente_base", "sans-serif")
        icon = styles.get("icono", "star")
        anim = styles.get("animacion", "fade")
        return (
            "const Profile = () => (\n"
            "  <div className=\"profile\">\n"
            f"    <i className=\"icon-{icon} {anim}\" "
            f"style={{color: '{color}', fontFamily: '{font}'}} />\n"
            "  </div>\n"
            ");"
        )


class ProfileEngine:
    """High level interface for generating design code from a profile token."""

    def __init__(self, translator: TranslationLayer | None = None) -> None:
        self.translator = translator or TranslationLayer()

    def translate(self, profile: Union[SymbolicProfile, Dict[str, str]]) -> Dict[str, str]:
        """Translate a profile token into design variables."""
        if isinstance(profile, SymbolicProfile):
            token = profile.to_token()
        else:
            token = profile
        return generate_styles(token)

    def generate_code(self, profile: Union[SymbolicProfile, Dict[str, str]]) -> Dict[str, str]:
        """Generate CSS and React snippets for the given profile."""
        styles = self.translate(profile)
        css = self.translator.to_css(styles)
        react = self.translator.to_react(styles)
        return {"styles": styles, "css": css, "react": react}

__all__ = ["TranslationLayer", "ProfileEngine"]

