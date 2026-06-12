"""Premium dark theme tokens for SUCHNA AI."""

DARK_THEME = {
    "bg": "#070B14",
    "sidebar": "#0F172A",
    "card": "#111827",
    "card_solid": "#111827",
    "card_glass": "rgba(17, 24, 39, 0.72)",
    "border": "rgba(148, 163, 184, 0.12)",
    "border_hover": "rgba(139, 92, 246, 0.4)",
    "primary": "#8B5CF6",
    "secondary": "#3B82F6",
    "accent": "#EC4899",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "text": "#FFFFFF",
    "text_muted": "#94A3B8",
    "text_subtle": "#64748B",
    "input_bg": "rgba(17, 24, 39, 0.85)",
    "shadow": "0 8px 32px rgba(0, 0, 0, 0.45)",
    "shadow_lg": "0 20px 60px rgba(0, 0, 0, 0.55)",
    "shadow_glow": "0 0 40px rgba(139, 92, 246, 0.15)",
    "app_gradient": (
        "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139, 92, 246, 0.18), transparent), "
        "radial-gradient(ellipse 60% 40% at 100% 0%, rgba(59, 130, 246, 0.12), transparent), "
        "radial-gradient(ellipse 50% 30% at 0% 100%, rgba(236, 72, 153, 0.08), transparent), "
        "#070B14"
    ),
    "glass_blur": "blur(20px)",
    "hero_gradient": "linear-gradient(135deg, #8B5CF6 0%, #6366F1 35%, #3B82F6 65%, #EC4899 100%)",
    "hero_mesh": (
        "radial-gradient(at 40% 20%, rgba(139, 92, 246, 0.45) 0px, transparent 50%), "
        "radial-gradient(at 80% 0%, rgba(59, 130, 246, 0.35) 0px, transparent 50%), "
        "radial-gradient(at 0% 50%, rgba(236, 72, 153, 0.25) 0px, transparent 50%), "
        "linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 70%, #7c3aed 100%)"
    ),
    "stat_grad_1": "linear-gradient(145deg, rgba(139, 92, 246, 0.18) 0%, rgba(17, 24, 39, 0.95) 100%)",
    "stat_grad_2": "linear-gradient(145deg, rgba(236, 72, 153, 0.16) 0%, rgba(17, 24, 39, 0.95) 100%)",
    "stat_grad_3": "linear-gradient(145deg, rgba(59, 130, 246, 0.18) 0%, rgba(17, 24, 39, 0.95) 100%)",
    "stat_grad_4": "linear-gradient(145deg, rgba(16, 185, 129, 0.16) 0%, rgba(17, 24, 39, 0.95) 100%)",
    "nav_active": "linear-gradient(135deg, rgba(139, 92, 246, 0.22) 0%, rgba(59, 130, 246, 0.12) 100%)",
}


def get_theme_tokens():
    """Returns the premium dark theme color tokens."""
    return DARK_THEME
