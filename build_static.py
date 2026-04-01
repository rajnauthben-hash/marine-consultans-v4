from __future__ import annotations

import html
import shutil
import struct
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"


TAILWIND_CONFIG = """
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "surface": "#f4faff",
        "surface-container-lowest": "#ffffff",
        "surface-container-low": "#e9f6fd",
        "surface-container": "#e3f0f8",
        "surface-container-high": "#ddeaf2",
        "surface-container-highest": "#d7e4ec",
        "surface-variant": "#d7e4ec",
        "background": "#f4faff",
        "primary": "#001628",
        "primary-container": "#002b47",
        "secondary": "#48626e",
        "secondary-container": "#cbe7f5",
        "tertiary": "#280c00",
        "tertiary-container": "#481c00",
        "on-primary": "#ffffff",
        "on-primary-container": "#6a94bc",
        "on-secondary": "#ffffff",
        "on-secondary-container": "#304a55",
        "on-surface": "#111d23",
        "on-surface-variant": "#42474d",
        "on-tertiary-container": "#eb6a00",
        "outline": "#73777e",
        "outline-variant": "#c3c7ce"
      },
      fontFamily: {
        "headline": ["Manrope"],
        "body": ["Inter"],
        "label": ["Inter"]
      },
      boxShadow: {
        "soft": "0 18px 48px rgba(17, 29, 35, 0.08)",
        "hero": "0 30px 70px rgba(0, 22, 40, 0.28)"
      }
    }
  }
}
""".strip()


SITE_CSS = dedent(
    """
    :root { color-scheme: light; }
    body { font-family: "Inter", sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: "Manrope", sans-serif; }
    .material-symbols-outlined { font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24; line-height: 1; vertical-align: middle; }
    .hero-gradient { background: linear-gradient(135deg, rgba(0, 22, 40, 0.98), rgba(0, 43, 71, 0.9)), radial-gradient(circle at top right, rgba(235, 106, 0, 0.18), transparent 28%); }
    .panel-glow { box-shadow: 0 30px 70px rgba(0, 22, 40, 0.18); }
    .menu-panel { opacity: 0; pointer-events: none; transform: translateY(10px); transition: opacity 0.18s ease, transform 0.18s ease; }
    .menu-group:hover .menu-panel, .menu-group:focus-within .menu-panel { opacity: 1; pointer-events: auto; transform: translateY(0); }
    .mobile-menu[hidden] { display: none !important; }
    .filter-chip-active { background: #001628; color: white; border-color: #001628; }
    .is-hidden { display: none !important; }
    .toast { position: fixed; right: 1rem; bottom: 1rem; z-index: 100; max-width: 24rem; border-left: 4px solid #eb6a00; background: rgba(255, 255, 255, 0.96); color: #111d23; padding: 1rem 1.125rem; box-shadow: 0 24px 50px rgba(17, 29, 35, 0.18); }
    .toast strong { display: block; margin-bottom: 0.25rem; font-family: "Manrope", sans-serif; }
    """
).strip()


SITE_JS = dedent(
    """
    (() => {
      const showToast = (title, body) => {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = 'toast rounded-lg';
        toast.innerHTML = `<strong>${title}</strong><span>${body}</span>`;
        document.body.appendChild(toast);
        window.setTimeout(() => toast.remove(), 4200);
      };

      const toggle = document.querySelector('[data-mobile-toggle]');
      const mobileMenu = document.querySelector('[data-mobile-menu]');
      if (toggle && mobileMenu) {
        toggle.addEventListener('click', () => {
          const isHidden = mobileMenu.hasAttribute('hidden');
          if (isHidden) mobileMenu.removeAttribute('hidden');
          else mobileMenu.setAttribute('hidden', '');
          toggle.setAttribute('aria-expanded', String(isHidden));
        });
      }

      document.querySelectorAll('[data-toast-title]').forEach((button) => {
        button.addEventListener('click', (event) => {
          event.preventDefault();
          showToast(
            button.getAttribute('data-toast-title') || 'Action captured',
            button.getAttribute('data-toast-body') || 'This placeholder action is ready for real business input.'
          );
        });
      });

      document.querySelectorAll('form[data-demo-form]').forEach((form) => {
        form.addEventListener('submit', (event) => {
          event.preventDefault();
          if (!form.reportValidity()) return;
          showToast(
            form.getAttribute('data-success-title') || 'Form submitted',
            form.getAttribute('data-success-body') || 'This local demo captures the expected submission state without a backend endpoint.'
          );
          form.reset();
        });
      });

      document.querySelectorAll('[data-filter-root]').forEach((root) => {
        const input = root.querySelector('[data-filter-search]');
        const buttons = Array.from(root.querySelectorAll('[data-filter-button]'));
        const items = Array.from(root.querySelectorAll('[data-filter-item]'));
        let activeFilter = 'all';

        const applyFilter = () => {
          const query = (input?.value || '').trim().toLowerCase();
          items.forEach((item) => {
            const text = (item.getAttribute('data-filter-item') || '').toLowerCase();
            const groups = (item.getAttribute('data-filter-groups') || '').toLowerCase().split(',');
            const matchesQuery = !query || text.includes(query);
            const matchesGroup = activeFilter === 'all' || groups.some((group) => group.trim() === activeFilter);
            item.classList.toggle('is-hidden', !(matchesQuery && matchesGroup));
          });
        };

        buttons.forEach((button) => {
          button.addEventListener('click', () => {
            activeFilter = button.getAttribute('data-filter-button') || 'all';
            buttons.forEach((entry) => entry.classList.remove('filter-chip-active'));
            button.classList.add('filter-chip-active');
            applyFilter();
          });
        });

        input?.addEventListener('input', applyFilter);
        applyFilter();
      });
    })();
    """
).strip()


VERCEL_CONFIG = dedent(
    """
    {
      "cleanUrls": true,
      "trailingSlash": false,
      "redirects": [
        { "source": "/quote", "destination": "/request-quote.html", "permanent": true },
        { "source": "/quote.html", "destination": "/request-quote.html", "permanent": true },
        { "source": "/support", "destination": "/services/support-request.html", "permanent": true },
        { "source": "/support.html", "destination": "/services/support-request.html", "permanent": true },
        { "source": "/industries", "destination": "/about.html", "permanent": true },
        { "source": "/industries.html", "destination": "/about.html", "permanent": true }
      ]
    }
    """
).strip() + "\n"


CORE_NAV = [
    ("Home", "/index.html", "home"),
    ("About", "/about.html", "about"),
    ("Catalogue / Resources", "/resources.html", "resources"),
    ("News / Updates", "/news.html", "news"),
    ("Contact", "/contact.html", "contact"),
]


PRODUCT_CATEGORY_ORDER = [
    "liferafts-evacuation-systems",
    "lifeboats-davits-rescue-craft",
    "marine-safety-products",
    "navigation-aids",
    "marine-electronics",
    "chains-ropes-rigging",
    "charts-publications-instruments",
    "fire-safety-equipment",
    "engines-marine-power-systems",
]


SERVICE_ORDER = [
    "inspection-services",
    "maintenance-support",
    "certification-support",
    "safety-equipment-servicing",
    "procurement-supply-support",
    "technical-assistance",
    "support-request",
]


IMAGE_HOME = "https://lh3.googleusercontent.com/aida-public/AB6AXuD2evcTopGQhSIY0cUdCXg5Y2pWUNrH3I7vmX_A5kikicPJx6pA9xLbyQQU7kJU8mGryC-ukCLKbZUlXe4_c2tJquLpYsFNcYp2Pxzi63ldMm0W09F3ReEQvkh4Bq3XbhThLeGQlInoiW7unJGvGqhaieGWg8OUKUzpngIszSRiLcGExgqG_aEfarmm4WwRCHzKOJ3Wi0JVuC2kqeoXCsSb5OI5iGzKmHgIIXGN46dPsi0fUAPmBxwyZI6xPOgcFEdo6eCNsJ06enQv"
IMAGE_ABOUT = "https://lh3.googleusercontent.com/aida-public/AB6AXuBjk1gYW5rFxKf-hC6np-VjPG-NZBkdrlV__YmIugp4lLuyRcMMkfZGXWSp1mfuWjlGeMwVMlbmKztzhj4EJsL27QG9ahj5S2sclQac7XJ1NcCSap8jBpd-XE4ubuWqyE52G5j3rRLnj2lG2RYYQOvSjsqA5Bc2OktOAXmTcm3k1cx7l3USdTbcYX0JL7vuS3k9WOpL2bxhD8myvTfewHzRw5bV6QYZwwYlVqS0ekCqWIJnar5GU1oqqgUVd4b93feQpEjbCF-yqk3j"
IMAGE_PRODUCTS = "https://lh3.googleusercontent.com/aida-public/AB6AXuD4Bbfn8YnQR6nIUyjgAIH-zkV_qLGEdwVmKYHKe6j_od7IbDAHhLumHQoASKkg8xo-YHeFXU6Os3_UOErL80oar7sm_TPdWWc034ymwfER9RJbPU3xa8smGewRy1vV3UM9I-UArf762ubMTxkGu5_bW9CHuOyn9BPHjEpNn41sbsQ1aADK1AUOwZ-b538MU4IcxvR7JoWEjhjTRm5bnS_WXdvlbiDZjunbJfwqdVoiX-nSzyDHZi2AVP06QFfRfbCf98xf5w8ewO9H"
IMAGE_SERVICES = "https://lh3.googleusercontent.com/aida-public/AB6AXuAcvsi_0XvoLsvLH5d1j9gRvThn9zWg_ApDudHKTdyWIWwJRvBmll8ObhSVETBtNmsoW3teuKGrMub39gjgFhVeOsdz87pu2jZP1mOc2nPXm0LfLErfR8WDpe_4d1_QRO8kvduCqFwFN6fKMgXYMBc8ppEWQnWC61zNfT-z8iopR4YoyDxyxONPgrA1piRFspOzklHq9L_OzGOvB0H2BRdCpVtSL0k2ZjVSQenJ8G6dovo6rq3qqVRCsl4s33WQfT9JIiS8KjhAt-ev"
IMAGE_RESOURCES = "https://lh3.googleusercontent.com/aida-public/AB6AXuDFwuHBGTDB5f-PbFNhjPVvlT_T1WRsmAOLBwHdChr9luHC1fNsry-VzfR0XieMcywtalOJ90zdrv3BdcfdNRIkU-X-odQCPi6d2JUYV0GMNyBDJ1uQTlfUJS9ZviJpzm2dsL1SpTdG5fT8n9cbp7wjCBa2DMgT_xS8rfZCuliOd3E4a1YHDqzDij31myMoQAX5bbBwThkWCJUtUW2ALs9IXklxhzF-9x3dRdmfS82c1y7aWk_aG4ZMQCccgU6HtpzYWWtfJy-aCKjy"
IMAGE_NEWS = "https://lh3.googleusercontent.com/aida-public/AB6AXuAFyoL-JTqCpzE3Fn6hCVdlN-jR5S_2gB_9KmGdyv1HyhKPKlYUHFKGQGK5Bx2zumGCmpMqEYaDM0GBP3R3CNkOTchyZThkozfmF-76jZ3XHo9MZXVD33AeuFxu075ydbhVNzB-BCZjJWv07AkZwn0p8bZuASkgRPyRnK1v6VxOxQioAR8BZ8j5P61fKRRq6k1JTc12ldqEHqdAG8_GfjEREAgYLJ0a8E_NC3ztpKIo1RhLlaZ615Dxpp1RI80S_XNExDC1yMxsZ5Ff"
IMAGE_CONTACT = "https://lh3.googleusercontent.com/aida-public/AB6AXuAbE41DlK_J0jC1AAoYLvcgGSnhKOdEzCQjaZyq00tSbVrt1aKGuajEA7seEQnNxrghA8VlnoDtReUhpH7Nr28CNghY7n5r75i_WyL1HFkExiAFM1AQ-zMwQN02Z8St1VNc9DIuxmDljuOu_qqli9eEKbv4xH6O1y11lLyvjcANZshyUvzgLbhhKtSsxDjigg6MjD-iyHoJgJkHLeDhtxy-LeRH_QAks0zUTcGRQ-hUDVePpvZ4j9ZqenA9JPB6tBhgDHeeUsD0FRtX"
IMAGE_QUOTE = "https://lh3.googleusercontent.com/aida-public/AB6AXuDFwuHBGTDB5f-PbFNhjPVvlT_T1WRsmAOLBwHdChr9luHC1fNsry-VzfR0XieMcywtalOJ90zdrv3BdcfdNRIkU-X-odQCPi6d2JUYV0GMNyBDJ1uQTlfUJS9ZviJpzm2dsL1SpTdG5fT8n9cbp7wjCBa2DMgT_xS8rfZCuliOd3E4a1YHDqzDij31myMoQAX5bbBwThkWCJUtUW2ALs9IXklxhzF-9x3dRdmfS82c1y7aWk_aG4ZMQCccgU6HtpzYWWtfJy-aCKjy"
IMAGE_PRODUCT_DETAIL = "https://lh3.googleusercontent.com/aida-public/AB6AXuCne8Jg0-hjJ-L5lbFONC8lTyTALiUWRL1GG8sBPy72Krp14H0HFe_Esmw_nU5DlromfNu2xMQGqudZIjc06IOgW6fA_fNfV3anDnrXcA3kYE63bWV_FAyvJq7PSlKVe8XCvi-GNM-n2MS1QkaHMUN9LhU9KzcxxT5oaQdOeLSZJeQlEUfzV255YirshVv95OEWcj-YxUiyDmuvHbkb_xZuxkWhTpPTHAT_9KxWH5NeEvWYlMRCy2qvd9ePquf6WqimkuyqeWG7wYms"


@dataclass(frozen=True)
class Category:
    slug: str
    title: str
    icon: str
    summary: str
    overview: str
    groups: tuple[str, ...]
    representative_products: tuple[str, ...]
    related: tuple[str, ...]

    @property
    def path(self) -> str:
        return f"/categories/{self.slug}.html"


@dataclass(frozen=True)
class Service:
    slug: str
    title: str
    icon: str
    summary: str
    overview: str
    scope: tuple[str, ...]
    audience: tuple[str, ...]
    related: tuple[str, ...]

    @property
    def path(self) -> str:
        return f"/services/{self.slug}.html"


CATEGORY_DATA = {
    "liferafts-evacuation-systems": Category(
        "liferafts-evacuation-systems",
        "Liferafts & Evacuation Systems",
        "emergency",
        "Emergency evacuation products for commercial vessels, offshore assets, and passenger support craft operating in Trinidad & Tobago and the wider Caribbean.",
        "This category supports vessel operators who need dependable evacuation equipment, repacking support coordination, and procurement guidance for raft systems and launch accessories. Verified approval details should be inserted after supplier and class documentation is confirmed.",
        ("Throw-over liferafts", "Canister-packed liferafts", "Hydrostatic release units", "Evacuation accessories"),
        ("Liferaft canisters", "Cradles and lashings", "MES accessories", "Service kits"),
        ("marine-safety-products", "lifeboats-davits-rescue-craft", "fire-safety-equipment"),
    ),
    "lifeboats-davits-rescue-craft": Category(
        "lifeboats-davits-rescue-craft",
        "Lifeboats, Davits & Rescue Craft",
        "directions_boat",
        "Launch and recovery equipment for vessel safety programs, offshore installations, and workboat support fleets.",
        "Use this section to manage procurement and service coordination for lifeboats, davits, rescue boats, winches, and supporting spare parts. Final approved makes, models, and certification records should be inserted during business review.",
        ("Rescue boats", "Lifeboat release gear", "Davit systems", "Launch controls and spare parts"),
        ("Winch assemblies", "Hooks and release units", "Operator seats", "Control and brake components"),
        ("liferafts-evacuation-systems", "marine-safety-products", "engines-marine-power-systems"),
    ),
    "marine-safety-products": Category(
        "marine-safety-products",
        "Marine Safety Products",
        "health_and_safety",
        "General vessel safety equipment and protective gear for crews, contractors, and marine operations teams.",
        "This category is intended for lifejackets, immersion suits, PPE, distress signaling equipment, and portable emergency gear. Replace the placeholder compliance notes with verified approval data before final commercial use.",
        ("Lifejackets and buoyancy aids", "Immersion suits", "Emergency signaling", "Crew PPE"),
        ("Lifejackets", "Throwable devices", "EPIRB and strobe accessories", "Protective helmets and gloves"),
        ("liferafts-evacuation-systems", "fire-safety-equipment", "navigation-aids"),
    ),
    "navigation-aids": Category(
        "navigation-aids",
        "Navigation Aids",
        "assistant_navigation",
        "Visual and electronic aids that support channel marking, coastal guidance, and vessel positioning programs.",
        "Navigation aids are often project-specific, so this page is structured as a procurement and inquiry template. Confirm project drawings, battery requirements, and approval criteria before populating final product lines.",
        ("Buoys and markers", "Solar lantern systems", "Daymarks and signage", "Mounting hardware"),
        ("Marine lanterns", "Buoy bodies", "Marker posts", "Control enclosures"),
        ("marine-electronics", "charts-publications-instruments", "marine-safety-products"),
    ),
    "marine-electronics": Category(
        "marine-electronics",
        "Marine Electronics",
        "radar",
        "Bridge and communication equipment for regional vessel support, retrofits, and replacement cycles.",
        "Use this category for communication systems, bridge displays, sensors, alarms, and supporting marine electronics procurement. Insert verified OEM compatibility and approval data when actual vendor selections are approved.",
        ("Communication systems", "Bridge displays", "Sensors and alarms", "Power and interface accessories"),
        ("VHF radios", "AIS transponders", "Radar displays", "Autopilot accessories"),
        ("navigation-aids", "charts-publications-instruments", "engines-marine-power-systems"),
    ),
    "chains-ropes-rigging": Category(
        "chains-ropes-rigging",
        "Chains, Ropes & Rigging",
        "anchor",
        "Mooring, lifting, and rigging products for port operations, deck work, offshore support, and technical supply programs.",
        "This category covers ropes, wire, chain, shackles, slings, hooks, and rigging hardware. Load ratings, certificates, and supplier batch details should be confirmed before technical issue or quotation.",
        ("Mooring ropes", "Anchor chains", "Rigging hardware", "Lifting accessories"),
        ("Nylon hawsers", "Wire rope slings", "Turnbuckles and shackles", "Hooks and swivels"),
        ("engines-marine-power-systems", "marine-safety-products", "products/viking-braidline-nylon-super-hawser"),
    ),
    "charts-publications-instruments": Category(
        "charts-publications-instruments",
        "Charts, Publications & Instruments",
        "menu_book",
        "Bridge reference materials and precision instruments that support voyage planning, onboard compliance, and technical inspections.",
        "Use this page for navigation publications, charts, inspection instruments, and bridge-room consumables. Availability and edition control should be updated during manual content review.",
        ("Paper and digital charts", "Publications and manuals", "Inspection instruments", "Measurement accessories"),
        ("Nautical publications", "Binoculars and compasses", "Calipers and gauges", "Weather instruments"),
        ("navigation-aids", "marine-electronics", "marine-safety-products"),
    ),
    "fire-safety-equipment": Category(
        "fire-safety-equipment",
        "Fire Safety Equipment",
        "fire_extinguisher",
        "Portable and fixed fire safety products for engine rooms, accommodations, workshops, and offshore support environments.",
        "This category supports procurement and servicing coordination for extinguishers, hoses, valves, detection accessories, and fixed-system consumables. Insert approved service schedules and compliance references when they are confirmed.",
        ("Portable extinguishers", "Hose and nozzle sets", "Detection accessories", "Fixed-system consumables"),
        ("Cylinder assemblies", "Hose reels", "Cabinet fittings", "Refill and test accessories"),
        ("marine-safety-products", "liferafts-evacuation-systems", "services/safety-equipment-servicing"),
    ),
    "engines-marine-power-systems": Category(
        "engines-marine-power-systems",
        "Engines / Marine Power Systems",
        "settings",
        "Propulsion and auxiliary equipment support for repair planning, overhaul procurement, and technical vessel assistance.",
        "This category is structured for engine spares, generator parts, filtration, seals, pumps, and supporting components. Populate OEM references, dimensions, and stock positions only after manual verification.",
        ("Engine spares", "Auxiliary systems", "Filters and consumables", "Powertrain accessories"),
        ("Pump kits", "Seals and gaskets", "Turbocharger spares", "Generator support items"),
        ("marine-electronics", "chains-ropes-rigging", "services/maintenance-support"),
    ),
}


SERVICE_DATA = {
    "inspection-services": Service(
        "inspection-services",
        "Inspection Services",
        "fact_check",
        "Field inspection support for marine assets, safety equipment programs, and technical condition reviews.",
        "This service page is designed for inspection coordination, survey planning, condition checks, and documentation support. Verified scope boundaries, approvals, and named standards should be inserted during business review.",
        ("Visual inspection planning", "Condition reporting", "Equipment checks", "Documentation support"),
        ("Vessel operators", "Marine contractors", "Port and terminal teams", "Procurement and technical managers"),
        ("maintenance-support", "certification-support", "support-request"),
    ),
    "maintenance-support": Service(
        "maintenance-support",
        "Maintenance Support",
        "build",
        "Planned and corrective support for vessels, support craft, and marine equipment programs.",
        "Use this page for maintenance coordination, replacement part planning, workshop support, and field assistance requests. Final response coverage, locations, and turnaround expectations should be approved before publication.",
        ("Planned maintenance coordination", "Corrective work support", "Consumables and spare parts", "Workshop and onboard assistance"),
        ("Vessel engineers", "Fleet managers", "Operations coordinators", "Marine suppliers"),
        ("inspection-services", "procurement-supply-support", "technical-assistance"),
    ),
    "certification-support": Service(
        "certification-support",
        "Certification Support",
        "verified",
        "Administrative and technical support for documentation packages, audits, and submission readiness.",
        "This page avoids unverified certification claims and instead frames the service as preparation support. Insert only confirmed authorities, certificates, and approved partner relationships after manual validation.",
        ("Document package review", "Audit readiness support", "Submission coordination", "Record control guidance"),
        ("Operations managers", "Quality teams", "Port service coordinators", "Project procurement teams"),
        ("inspection-services", "safety-equipment-servicing", "support-request"),
    ),
    "safety-equipment-servicing": Service(
        "safety-equipment-servicing",
        "Safety Equipment Servicing",
        "health_and_safety",
        "Support for inspection cycles, replacement planning, and servicing coordination for vessel safety equipment.",
        "Use this page as the active route for life-saving appliance and fire safety servicing inquiries. Confirm service stations, approved brands, and local inspection capabilities before adding final operating claims.",
        ("Inspection cycle coordination", "Replacement and replenishment planning", "Workshop scheduling", "Service report follow-up"),
        ("Ship operators", "Safety officers", "Marine procurement teams", "Offshore support vessels"),
        ("certification-support", "inspection-services", "support-request"),
    ),
    "procurement-supply-support": Service(
        "procurement-supply-support",
        "Procurement / Supply Support",
        "inventory_2",
        "B2B sourcing support for marine products, technical stores, and maintenance requirements.",
        "This service is positioned around technical procurement and vendor coordination rather than unsupported broad marketing claims. Add supplier lists, stock ranges, and logistics workflows only after approval.",
        ("Specification review", "Supplier coordination", "Commercial comparison support", "Delivery follow-up"),
        ("Purchasing departments", "Fleet support teams", "Ship chandlers", "Project coordinators"),
        ("technical-assistance", "maintenance-support", "support-request"),
    ),
    "technical-assistance": Service(
        "technical-assistance",
        "Technical Assistance",
        "engineering",
        "General technical coordination for product selection, replacement planning, and service scoping.",
        "This page supports customers who need help matching products or service paths to vessel requirements. Use it as the general route for questions that are not yet ready for a formal quote.",
        ("Requirement review", "Product and service matching", "Documentation guidance", "Escalation to quote or service inquiry"),
        ("Technical buyers", "Chief engineers", "Operations staff", "Regional vessel support teams"),
        ("procurement-supply-support", "inspection-services", "support-request"),
    ),
    "support-request": Service(
        "support-request",
        "Support Request / Service Inquiry",
        "support_agent",
        "A direct route for service-related requests that need triage before quoting or dispatch planning.",
        "Use this route for open support needs, vessel assistance requests, and service follow-up. Contact windows, escalation details, and after-hours protocols remain placeholders until the business confirms them.",
        ("General service intake", "Scope clarification", "Escalation to technical teams", "Follow-up coordination"),
        ("Operations contacts", "Marine supervisors", "Safety managers", "Procurement teams"),
        ("technical-assistance", "maintenance-support", "certification-support"),
    ),
}


NEWS_ITEMS = (
    ("Operations Update Placeholder", "Regional vessel support and delivery updates can be published here once approved by the business team.", "Operations"),
    ("Product Availability Update Placeholder", "Use this card for approved stock notices, incoming shipments, or temporary supply constraints.", "Products"),
    ("Service Bulletin Placeholder", "This space can hold workshop notices, service schedules, or inspection campaign announcements.", "Service"),
)


RESOURCE_ITEMS = (
    ("Marine Product Catalogue", "Catalogue Download Placeholder", "Catalog"),
    ("Service Capability Brief", "Service Description Placeholder", "Services"),
    ("Compliance Reference Pack", "Compliance Information Placeholder", "Compliance"),
    ("Company Profile", "Company Overview Placeholder", "Company"),
)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def link_button(label: str, href: str, *, kind: str = "primary", attrs: str = "") -> str:
    base = "inline-flex items-center justify-center gap-2 rounded-md px-6 py-3 text-sm font-bold tracking-wide transition-all"
    if kind == "primary":
        classes = f"{base} bg-tertiary-container text-on-tertiary-container hover:brightness-110"
    elif kind == "secondary":
        classes = f"{base} border border-white/20 text-white hover:bg-white/10"
    elif kind == "surface":
        classes = f"{base} border border-primary text-primary hover:bg-primary hover:text-white"
    else:
        classes = f"{base} bg-surface-container-low text-primary hover:bg-surface-container"
    return f'<a class="{classes}" href="{escape(href)}" {attrs}>{escape(label)}</a>'


def render_header(current: str) -> str:
    def nav_link(label: str, href: str, key: str) -> str:
        active = current == key
        classes = (
            "text-primary border-b-2 border-on-tertiary-container pb-1"
            if active
            else "text-on-surface-variant hover:text-primary"
        )
        return f'<a class="{classes} text-sm font-bold tracking-tight transition-colors" href="{escape(href)}">{escape(label)}</a>'

    product_links = "".join(
        f'<a class="block rounded-md px-3 py-2 text-sm text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(CATEGORY_DATA[slug].path)}">{escape(CATEGORY_DATA[slug].title)}</a>'
        for slug in PRODUCT_CATEGORY_ORDER
    )
    service_links = "".join(
        f'<a class="block rounded-md px-3 py-2 text-sm text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(SERVICE_DATA[slug].path)}">{escape(SERVICE_DATA[slug].title)}</a>'
        for slug in SERVICE_ORDER
    )
    product_classes = "text-primary border-b-2 border-on-tertiary-container pb-1" if current == "products" else "text-on-surface-variant hover:text-primary"
    service_classes = "text-primary border-b-2 border-on-tertiary-container pb-1" if current == "services" else "text-on-surface-variant hover:text-primary"

    mobile_primary_links = "".join(
        (
            f'<a class="block rounded-md px-3 py-2 text-sm font-semibold text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(href)}">{escape(label)}</a>'
        )
        for label, href in (
            ("Home", "/index.html"),
            ("About", "/about.html"),
            ("Products", "/products.html"),
            ("Services", "/services.html"),
            ("Catalogue / Resources", "/resources.html"),
            ("News / Updates", "/news.html"),
            ("Contact", "/contact.html"),
        )
    )
    mobile_product_links = "".join(
        f'<a class="block rounded-md px-3 py-2 text-sm text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(CATEGORY_DATA[slug].path)}">{escape(CATEGORY_DATA[slug].title)}</a>'
        for slug in PRODUCT_CATEGORY_ORDER
    )
    mobile_service_links = "".join(
        f'<a class="block rounded-md px-3 py-2 text-sm text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(SERVICE_DATA[slug].path)}">{escape(SERVICE_DATA[slug].title)}</a>'
        for slug in SERVICE_ORDER
    )
    inquiry_links = "".join(
        (
            f'<a class="block rounded-md px-3 py-2 text-sm text-on-surface-variant hover:bg-surface-container-low hover:text-primary" href="{escape(href)}">{escape(label)}</a>'
        )
        for label, href in (
            ("General Contact", "/contact.html"),
            ("Product Inquiry", "/inquiries/product-inquiry.html"),
            ("Service Inquiry", "/inquiries/service-inquiry.html"),
            ("Request a Quote", "/request-quote.html"),
        )
    )

    return dedent(
        f"""
        <header class="fixed inset-x-0 top-0 z-50 border-b border-slate-200 bg-slate-50/85 backdrop-blur-xl">
          <div class="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4">
            <a class="text-xl font-extrabold uppercase tracking-tighter text-primary" href="/index.html">Marine Consultants</a>
            <nav class="hidden xl:flex items-center gap-6">
              {nav_link("Home", "/index.html", "home")}
              {nav_link("About", "/about.html", "about")}
              <div class="menu-group relative">
                <a class="{product_classes} text-sm font-bold tracking-tight transition-colors" href="/products.html">Products</a>
                <div class="menu-panel absolute left-0 top-full mt-3 w-[21rem] rounded-xl border border-outline-variant bg-white p-4 shadow-soft">
                  <a class="mb-3 block rounded-md bg-surface-container-low px-3 py-2 text-sm font-bold text-primary" href="/products.html">Product Catalog Overview</a>
                  <div class="grid gap-1">{product_links}</div>
                  <div class="mt-3 border-t border-outline-variant pt-3">
                    <a class="block rounded-md px-3 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="/inquiries/product-inquiry.html">Product Inquiry</a>
                  </div>
                </div>
              </div>
              <div class="menu-group relative">
                <a class="{service_classes} text-sm font-bold tracking-tight transition-colors" href="/services.html">Services</a>
                <div class="menu-panel absolute left-0 top-full mt-3 w-[21rem] rounded-xl border border-outline-variant bg-white p-4 shadow-soft">
                  <a class="mb-3 block rounded-md bg-surface-container-low px-3 py-2 text-sm font-bold text-primary" href="/services.html">Services Overview</a>
                  <div class="grid gap-1">{service_links}</div>
                  <div class="mt-3 border-t border-outline-variant pt-3">
                    <a class="block rounded-md px-3 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="/inquiries/service-inquiry.html">Service Inquiry</a>
                  </div>
                </div>
              </div>
              {nav_link("Catalogue / Resources", "/resources.html", "resources")}
              {nav_link("News / Updates", "/news.html", "news")}
              {nav_link("Contact", "/contact.html", "contact")}
            </nav>
            <div class="flex items-center gap-3">
              <a class="hidden rounded-md bg-primary px-5 py-2.5 text-sm font-bold text-white transition-all hover:bg-primary-container md:inline-flex" href="/request-quote.html">Request a Quote</a>
              <button aria-expanded="false" aria-label="Toggle mobile menu" class="inline-flex h-11 w-11 items-center justify-center rounded-md border border-outline-variant text-primary xl:hidden" data-mobile-toggle type="button">
                <span class="material-symbols-outlined">menu</span>
              </button>
            </div>
          </div>
          <div class="mobile-menu border-t border-outline-variant bg-white xl:hidden" data-mobile-menu hidden>
            <div class="mx-auto max-w-7xl space-y-6 px-6 py-5">
              <div class="grid gap-1">
                {mobile_primary_links}
              </div>
              <div>
                <div class="mb-2 px-3 text-[11px] font-bold uppercase tracking-[0.18em] text-secondary">Product Categories</div>
                <div class="grid gap-1">{mobile_product_links}</div>
              </div>
              <div>
                <div class="mb-2 px-3 text-[11px] font-bold uppercase tracking-[0.18em] text-secondary">Service Links</div>
                <div class="grid gap-1">{mobile_service_links}</div>
              </div>
              <div>
                <div class="mb-2 px-3 text-[11px] font-bold uppercase tracking-[0.18em] text-secondary">Inquiry Paths</div>
                <div class="grid gap-1">{inquiry_links}</div>
              </div>
              <a class="inline-flex w-full items-center justify-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-white" href="/request-quote.html">Request a Quote</a>
            </div>
          </div>
        </header>
        """
    ).strip()


def render_footer() -> str:
    product_links = "".join(
        f'<a class="text-on-primary-container hover:text-white transition-colors" href="{escape(CATEGORY_DATA[slug].path)}">{escape(CATEGORY_DATA[slug].title)}</a>'
        for slug in PRODUCT_CATEGORY_ORDER
    )
    service_links = "".join(
        f'<a class="text-on-primary-container hover:text-white transition-colors" href="{escape(SERVICE_DATA[slug].path)}">{escape(SERVICE_DATA[slug].title)}</a>'
        for slug in SERVICE_ORDER
    )
    return dedent(
        f"""
        <footer class="mt-20 border-t border-primary-container bg-primary text-white">
          <div class="mx-auto grid max-w-7xl gap-12 px-6 py-16 md:grid-cols-2 xl:grid-cols-5">
            <div class="xl:col-span-2">
              <div class="mb-4 text-xl font-extrabold uppercase tracking-tighter">Marine Consultants</div>
              <p class="max-w-lg text-sm leading-relaxed text-on-primary-container">
                Trinidad & Tobago and regional marine supply, service support, inspections, maintenance coordination, and B2B inquiry management.
              </p>
              <div class="mt-6 space-y-2 text-sm text-on-primary-container">
                <div><strong class="text-white">Regional Base:</strong> Trinidad & Tobago / Caribbean support</div>
                <div><strong class="text-white">Contact Details:</strong> Contact Details Placeholder</div>
                <div><strong class="text-white">Compliance Notes:</strong> Compliance Information Placeholder</div>
              </div>
            </div>
            <div class="space-y-3 text-sm">
              <div class="text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Site</div>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/index.html">Home</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/about.html">About</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/products.html">Products</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/services.html">Services</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/resources.html">Catalogue / Resources</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/news.html">News / Updates</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/contact.html">Contact</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/request-quote.html">Request a Quote</a>
            </div>
            <div class="space-y-3 text-sm">
              <div class="text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Products</div>
              {product_links}
            </div>
            <div class="space-y-3 text-sm">
              <div class="text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Services</div>
              {service_links}
              <a class="text-on-primary-container hover:text-white transition-colors" href="/inquiries/product-inquiry.html">Product Inquiry</a>
              <a class="text-on-primary-container hover:text-white transition-colors" href="/inquiries/service-inquiry.html">Service Inquiry</a>
            </div>
          </div>
          <div class="border-t border-primary-container/80">
            <div class="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-5 text-xs text-on-primary-container md:flex-row md:items-center md:justify-between">
              <div>Final consolidated build generated from selected Stitch references and cleaned of duplicate active page variants.</div>
              <div class="flex gap-4">
                <a class="hover:text-white transition-colors" href="/privacy.html">Privacy</a>
                <a class="hover:text-white transition-colors" href="/terms.html">Terms</a>
              </div>
            </div>
          </div>
        </footer>
        """
    ).strip()


def render_page(title: str, description: str, section: str, body: str) -> str:
    return dedent(
        f"""
        <!DOCTYPE html>
        <html class="scroll-smooth" lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{escape(title)}</title>
            <meta name="description" content="{escape(description)}" />
            <link rel="icon" href="/favicon.ico" />
            <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
            <script>{TAILWIND_CONFIG}</script>
            <link rel="stylesheet" href="/assets/site.css" />
          </head>
          <body class="bg-surface text-on-surface">
            {render_header(section)}
            <main class="pt-20">{body}</main>
            {render_footer()}
            <script src="/assets/site.js"></script>
          </body>
        </html>
        """
    ).strip() + "\n"


def hero(
    eyebrow: str,
    title: str,
    copy: str,
    *,
    image_url: str,
    primary_href: str,
    primary_label: str,
    secondary_href: str | None = None,
    secondary_label: str | None = None,
    panel_title: str,
    panel_items: tuple[tuple[str, str], ...],
) -> str:
    panel_rows = "".join(
        f'<div class="flex items-center justify-between gap-4 border-b border-white/10 py-3 last:border-b-0"><span class="text-xs font-bold uppercase tracking-[0.18em] text-on-primary-container">{escape(label)}</span><span class="text-right text-sm font-semibold text-white">{escape(value)}</span></div>'
        for label, value in panel_items
    )
    secondary = link_button(secondary_label or "", secondary_href or "#", kind="secondary") if secondary_href and secondary_label else ""
    return dedent(
        f"""
        <section class="hero-gradient relative overflow-hidden py-24 md:py-32">
          <div class="absolute inset-0 opacity-25"><img alt="" class="h-full w-full object-cover" src="{escape(image_url)}" /></div>
          <div class="absolute inset-0 bg-gradient-to-r from-primary via-primary/90 to-transparent"></div>
          <div class="relative z-10 mx-auto grid max-w-7xl items-center gap-12 px-6 lg:grid-cols-12">
            <div class="lg:col-span-7">
              <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/8 px-4 py-1.5">
                <span class="material-symbols-outlined text-sm text-on-tertiary-container">location_on</span>
                <span class="text-xs font-bold uppercase tracking-[0.22em] text-white">{escape(eyebrow)}</span>
              </div>
              <h1 class="mb-6 text-5xl font-extrabold leading-[1.05] tracking-tight text-white md:text-7xl">{title}</h1>
              <p class="max-w-3xl text-lg leading-relaxed text-on-primary-container md:text-xl">{escape(copy)}</p>
              <div class="mt-10 flex flex-wrap gap-4">{link_button(primary_label, primary_href)}{secondary}</div>
            </div>
            <div class="lg:col-span-5">
              <div class="panel-glow rounded-2xl border border-white/10 bg-white/8 p-7 backdrop-blur-md">
                <div class="mb-4 text-xs font-bold uppercase tracking-[0.2em] text-on-tertiary-container">{escape(panel_title)}</div>
                {panel_rows}
              </div>
            </div>
          </div>
        </section>
        """
    ).strip()


def section_intro(eyebrow: str, title: str, copy: str, *, centered: bool = False) -> str:
    align = "mx-auto max-w-3xl text-center" if centered else "max-w-3xl"
    return f'<div class="{align} mb-12"><div class="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-secondary">{escape(eyebrow)}</div><h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary md:text-4xl">{escape(title)}</h2><p class="text-base leading-relaxed text-on-surface-variant md:text-lg">{escape(copy)}</p></div>'


def product_card(category: Category, *, compact: bool = False) -> str:
    description = category.summary if not compact else category.summary.split(".")[0] + "."
    groups = ",".join(word for word in category.slug.replace("-", " ").split() if word)
    return dedent(
        f"""
        <article class="flex h-full flex-col rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft transition-all hover:-translate-y-1 hover:shadow-xl" data-filter-item="{escape(category.title + ' ' + category.summary + ' ' + ' '.join(category.groups))}" data-filter-groups="{escape(groups)}">
          <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-surface-container text-primary">
            <span class="material-symbols-outlined text-3xl">{escape(category.icon)}</span>
          </div>
          <h3 class="mb-3 text-2xl font-bold text-primary">{escape(category.title)}</h3>
          <p class="mb-6 flex-grow text-sm leading-relaxed text-on-surface-variant">{escape(description)}</p>
          <div class="space-y-2 text-xs font-semibold uppercase tracking-[0.16em] text-secondary">
            <div>{escape(category.groups[0])}</div>
            <div>{escape(category.groups[1])}</div>
          </div>
          <div class="mt-6 flex flex-wrap gap-3">
            <a class="text-sm font-bold text-on-tertiary-container hover:text-primary" href="{escape(category.path)}">View category</a>
            <a class="text-sm font-bold text-primary hover:text-on-tertiary-container" href="/request-quote.html">Request quote</a>
          </div>
        </article>
        """
    ).strip()


def service_card(service: Service) -> str:
    return dedent(
        f"""
        <article class="flex h-full flex-col rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft transition-all hover:-translate-y-1 hover:shadow-xl">
          <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-surface-container text-primary">
            <span class="material-symbols-outlined text-3xl">{escape(service.icon)}</span>
          </div>
          <h3 class="mb-3 text-2xl font-bold text-primary">{escape(service.title)}</h3>
          <p class="mb-6 flex-grow text-sm leading-relaxed text-on-surface-variant">{escape(service.summary)}</p>
          <ul class="space-y-2 text-sm text-on-surface-variant">
            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">check_circle</span>{escape(service.scope[0])}</li>
            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">check_circle</span>{escape(service.scope[1])}</li>
          </ul>
          <div class="mt-6 flex flex-wrap gap-3">
            <a class="text-sm font-bold text-on-tertiary-container hover:text-primary" href="{escape(service.path)}">View service</a>
            <a class="text-sm font-bold text-primary hover:text-on-tertiary-container" href="/inquiries/service-inquiry.html">Service inquiry</a>
          </div>
        </article>
        """
    ).strip()


def support_paths() -> str:
    cards = (
        ("General Contact", "Share a general company, project, or procurement question with the regional team.", "/contact.html", "mail"),
        ("Product Inquiry", "Use this route when you already know the product category or need technical sourcing support.", "/inquiries/product-inquiry.html", "inventory"),
        ("Service Inquiry", "Use this route for inspections, maintenance, servicing, or open technical support needs.", "/inquiries/service-inquiry.html", "support_agent"),
        ("Request a Quote", "Use the main quote form for product, service, or bundled support requests.", "/request-quote.html", "description"),
    )
    cards_html = "".join(
        dedent(
            f"""
            <a class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-6 shadow-soft transition-all hover:-translate-y-1 hover:shadow-xl" href="{escape(href)}">
              <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-surface-container text-primary">
                <span class="material-symbols-outlined text-2xl">{escape(icon)}</span>
              </div>
              <h3 class="mb-3 text-xl font-bold text-primary">{escape(title)}</h3>
              <p class="text-sm leading-relaxed text-on-surface-variant">{escape(copy)}</p>
            </a>
            """
        ).strip()
        for title, copy, href, icon in cards
    )
    return dedent(
        f"""
        <section class="bg-surface px-6 py-24">
          <div class="mx-auto max-w-7xl">
            {section_intro("Inquiry Paths", "Choose the Right Contact Route", "The final build keeps the B2B inquiry flow clear so product, service, and quote requests do not compete with each other.", centered=True)}
            <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-4">{cards_html}</div>
          </div>
        </section>
        """
    ).strip()


def cta_band(title: str, copy: str, primary_label: str, primary_href: str, secondary_label: str, secondary_href: str) -> str:
    return dedent(
        f"""
        <section class="px-6 py-20">
          <div class="mx-auto max-w-7xl rounded-3xl bg-primary px-8 py-12 text-white shadow-hero md:px-12">
            <div class="grid items-center gap-8 md:grid-cols-[1.5fr,auto]">
              <div>
                <div class="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-on-tertiary-container">Regional Support</div>
                <h2 class="mb-4 text-3xl font-extrabold tracking-tight md:text-4xl">{escape(title)}</h2>
                <p class="max-w-3xl text-base leading-relaxed text-on-primary-container md:text-lg">{escape(copy)}</p>
              </div>
              <div class="flex flex-wrap gap-4">
                {link_button(primary_label, primary_href)}
                {link_button(secondary_label, secondary_href, kind="secondary")}
              </div>
            </div>
          </div>
        </section>
        """
    ).strip()


def grid_block(title: str, items: tuple[str, ...], icon: str) -> str:
    list_items = "".join(
        f'<li class="flex items-start gap-3 text-sm leading-relaxed text-on-surface-variant"><span class="material-symbols-outlined mt-0.5 text-secondary text-base">{escape(icon)}</span><span>{escape(item)}</span></li>'
        for item in items
    )
    return dedent(
        f"""
        <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
          <h3 class="mb-5 text-xl font-bold text-primary">{escape(title)}</h3>
          <ul class="space-y-3">{list_items}</ul>
        </div>
        """
    ).strip()


def form_field(label: str, field_html: str) -> str:
    return dedent(
        f"""
        <div class="space-y-2">
          <label class="block text-[11px] font-bold uppercase tracking-[0.18em] text-secondary">{escape(label)}</label>
          {field_html}
        </div>
        """
    ).strip()


def input_html(input_type: str, placeholder: str, *, required: bool = False, name: str = "") -> str:
    required_attr = " required" if required else ""
    name_attr = f' name="{escape(name)}"' if name else ""
    return f'<input class="w-full rounded-xl border-none bg-surface-container-low px-4 py-3 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container" type="{escape(input_type)}" placeholder="{escape(placeholder)}"{required_attr}{name_attr} />'


def textarea_html(placeholder: str, *, required: bool = False, name: str = "") -> str:
    required_attr = " required" if required else ""
    name_attr = f' name="{escape(name)}"' if name else ""
    return f'<textarea class="min-h-[10rem] w-full rounded-xl border-none bg-surface-container-low px-4 py-3 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container" placeholder="{escape(placeholder)}"{required_attr}{name_attr}></textarea>'


def select_html(options: tuple[str, ...], *, required: bool = False, name: str = "") -> str:
    required_attr = " required" if required else ""
    name_attr = f' name="{escape(name)}"' if name else ""
    option_html = "<option value=\"\">Select one</option>" + "".join(f'<option>{escape(option)}</option>' for option in options)
    return f'<select class="w-full rounded-xl border-none bg-surface-container-low px-4 py-3 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container"{required_attr}{name_attr}>{option_html}</select>'


def inquiry_form(
    *,
    title: str,
    intro: str,
    success_title: str,
    success_body: str,
    category_options: tuple[str, ...],
) -> str:
    fields = "\n".join(
        [
            form_field("Full Name", input_html("text", "Name", required=True, name="full_name")),
            form_field("Company", input_html("text", "Company name", required=True, name="company")),
            form_field("Email", input_html("email", "Email address", required=True, name="email")),
            form_field("Phone", input_html("tel", "Contact number", name="phone")),
            form_field("Category", select_html(category_options, required=True, name="category")),
            form_field("Project / Vessel Context", textarea_html("Share the vessel, product, service scope, location, and any schedule notes.", required=True, name="message")),
        ]
    )
    return dedent(
        f"""
        <section class="bg-surface px-6 py-24">
          <div class="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[0.9fr,1.1fr]">
            <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
              <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Inquiry Form</div>
              <h2 class="mb-4 text-3xl font-extrabold tracking-tight">{escape(title)}</h2>
              <p class="text-sm leading-relaxed text-on-primary-container">{escape(intro)}</p>
              <div class="mt-8 space-y-4 text-sm text-on-primary-container">
                <div><strong class="text-white">Contact Details:</strong> Contact Details Placeholder</div>
                <div><strong class="text-white">Regional Coverage:</strong> Trinidad & Tobago / Caribbean</div>
                <div><strong class="text-white">Documentation:</strong> Compliance Information Placeholder</div>
              </div>
            </div>
            <form class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft" data-demo-form data-success-body="{escape(success_body)}" data-success-title="{escape(success_title)}">
              <div class="grid gap-6 md:grid-cols-2">{fields}</div>
              <div class="mt-8"><button class="rounded-md bg-primary px-6 py-3 text-sm font-bold text-white hover:bg-primary-container" type="submit">Submit Inquiry</button></div>
            </form>
          </div>
        </section>
        """
    ).strip()


def render_home() -> str:
    categories = "".join(product_card(CATEGORY_DATA[slug], compact=True) for slug in PRODUCT_CATEGORY_ORDER)
    services = "".join(service_card(SERVICE_DATA[slug]) for slug in SERVICE_ORDER[:4])
    body = "\n".join(
        [
            hero(
                "Trinidad & Tobago / Caribbean marine support",
                "Regional Marine Supply & Service Support",
                "Marine Consultants Limited is positioned as a regional partner for marine supply, inspections, maintenance coordination, safety equipment servicing, certification support, and technical procurement.",
                image_url=IMAGE_HOME,
                primary_href="/products.html",
                primary_label="Browse Products",
                secondary_href="/services.html",
                secondary_label="View Services",
                panel_title="Core Positioning",
                panel_items=(
                    ("Focus", "Marine supply and service"),
                    ("Territory", "Trinidad & Tobago / Caribbean"),
                    ("Inquiry Flow", "B2B quote and support routes"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Services", "Operational Support Areas", "The strongest Stitch home layout is preserved here with a practical service overview and direct links into the final consolidated service structure.")}
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-4">{services}</div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                f"""
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl" data-filter-root>
                    {section_intro("Products", "Regional Product Categories", "The final build keeps the deeper product structure instead of flattening it into a generic catalog. Use the category pages to continue adding verified supplier and stock information.")}
                    <div class="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                      <input class="w-full rounded-xl border-none bg-surface-container-lowest px-5 py-4 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container md:max-w-md" data-filter-search placeholder="Search categories, product groups, or keywords..." type="search" />
                      <div class="flex flex-wrap gap-3">
                        <button class="filter-chip-active rounded-full border border-primary px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="all" type="button">All</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="safety" type="button">Safety</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="navigation" type="button">Navigation</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="engines" type="button">Power</button>
                      </div>
                    </div>
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{categories}</div>
                  </div>
                </section>
                """
            ).strip(),
            support_paths(),
            cta_band(
                "Need a consolidated quote path?",
                "The old Stitch variants mixed product CTAs, support requests, and general contact actions. The final site now routes them clearly so manual business follow-up stays organized.",
                "Request a Quote",
                "/request-quote.html",
                "Contact the Team",
                "/contact.html",
            ),
        ]
    )
    return render_page("Marine Consultants | Regional Marine Supply & Service", "Final consolidated home page for Marine Consultants with regional Trinidad & Tobago and Caribbean marine supply and service positioning.", "home", body)


def render_about() -> str:
    subcards = "".join(
        dedent(
            f"""
            <a class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft transition-all hover:-translate-y-1 hover:shadow-xl" href="{href}">
              <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-surface-container text-primary">
                <span class="material-symbols-outlined text-2xl">{icon}</span>
              </div>
              <h3 class="mb-3 text-xl font-bold text-primary">{title}</h3>
              <p class="text-sm leading-relaxed text-on-surface-variant">{copy}</p>
            </a>
            """
        ).strip()
        for title, copy, href, icon in (
            ("Company Overview", "Grounded regional positioning and editable profile content.", "/about/company-overview.html", "apartment"),
            ("Mission / Vision / Values", "One canonical operating-principles section kept on the main about page.", "/about.html#mission-vision-values", "flag"),
            ("Quality / Compliance", "A neutral compliance placeholder page that avoids unsupported approvals.", "/about/quality-compliance.html", "verified"),
            ("Leadership", "Leadership Placeholder content ready for approved biographies and roles.", "/about/leadership.html", "groups"),
        )
    )
    body = "\n".join(
        [
            hero(
                "Regional company profile",
                "About Marine Consultants",
                "The final about page keeps the established marine-industrial look while removing unsupported dates, staff totals, certification claims, and global marketing language.",
                image_url=IMAGE_ABOUT,
                primary_href="/about/company-overview.html",
                primary_label="View Company Overview",
                secondary_href="/contact.html",
                secondary_label="Contact the Team",
                panel_title="About Structure",
                panel_items=(
                    ("Coverage", "Trinidad & Tobago / Caribbean"),
                    ("Profile", "Company Overview Placeholder"),
                    ("Values", "Accuracy / responsiveness / safety"),
                    ("Leadership", "Leadership Placeholder"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Positioning", "Grounded Regional Framing", "Active about content now presents the business as a regional marine supply and service operation without unsupported legacy claims.")}
                    <div class="grid gap-6 lg:grid-cols-3">
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft lg:col-span-2">
                        <h3 class="mb-4 text-2xl font-bold text-primary">Company Overview Placeholder</h3>
                        <p class="mb-5 text-sm leading-relaxed text-on-surface-variant">
                          Use this section to add verified company history, ownership background, vessel support experience, and regional operating profile. The previous export contained conflicting dates and inflated authority language, so the final build keeps this deliberately neutral until approved business details are supplied.
                        </p>
                        <div class="grid gap-4 md:grid-cols-3">
                          <div class="rounded-xl bg-surface-container p-5"><div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Core Focus</div><div class="text-sm font-semibold text-primary">Marine supply, service, and procurement support</div></div>
                          <div class="rounded-xl bg-surface-container p-5"><div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Region</div><div class="text-sm font-semibold text-primary">Trinidad & Tobago / Caribbean</div></div>
                          <div class="rounded-xl bg-surface-container p-5"><div class="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Business Type</div><div class="text-sm font-semibold text-primary">B2B marine support</div></div>
                        </div>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-primary p-7 text-white shadow-hero" id="mission-vision-values">
                        <div class="mb-4 text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Mission / Vision / Values</div>
                        <ul class="space-y-4 text-sm leading-relaxed text-on-primary-container">
                          <li><strong class="text-white">Mission:</strong> Support vessel operators and marine buyers with practical regional supply and service coordination.</li>
                          <li><strong class="text-white">Vision:</strong> Build a clear, reliable regional support platform that customers can navigate easily.</li>
                          <li><strong class="text-white">Values:</strong> Accuracy, responsiveness, safety awareness, and maintainable documentation.</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                f"""
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Subpages / Sections", "Approved About Structure", "The about area is now split into clear canonical pages and one anchored operating-principles section so there is no ambiguity about which version is live.")}
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-4">{subcards}</div>
                  </div>
                </section>
                """
            ).strip(),
            cta_band(
                "Need to replace placeholders with real business details?",
                "The final build is ready for manual input on company history, leadership, and compliance notes without reopening the duplicate Stitch variants.",
                "Open Contact Page",
                "/contact.html",
                "Go to Resources",
                "/resources.html",
            ),
        ]
    )
    return render_page("About | Marine Consultants", "Canonical about page for the consolidated Marine Consultants website.", "about", body)


def render_products() -> str:
    cards = "".join(product_card(CATEGORY_DATA[slug]) for slug in PRODUCT_CATEGORY_ORDER)
    body = "\n".join(
        [
            hero(
                "Regional product catalog",
                "Marine Product Catalog",
                "The final product hub keeps the deeper category structure from the strongest Stitch concepts while removing unsupported stock claims and duplicate catalog variants.",
                image_url=IMAGE_PRODUCTS,
                primary_href="/request-quote.html",
                primary_label="Request a Quote",
                secondary_href="/resources.html",
                secondary_label="View Resources",
                panel_title="Catalog Notes",
                panel_items=(
                    ("Structure", "Nine core categories"),
                    ("Approach", "Category-led navigation"),
                    ("Status", "Manual product details remain editable"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl" data-filter-root>
                    {section_intro("Catalog", "Search and Filter the Final Product Structure", "This page now acts as the single approved product hub. Search and quick filters stay functional without introducing additional duplicate landing pages.")}
                    <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <input class="w-full rounded-xl border-none bg-surface-container-low px-5 py-4 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container lg:max-w-md" data-filter-search placeholder="Search products, categories, or key groups..." type="search" />
                      <div class="flex flex-wrap gap-3">
                        <button class="filter-chip-active rounded-full border border-primary px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="all" type="button">All</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="safety" type="button">Safety</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="navigation" type="button">Navigation</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="rigging" type="button">Rigging</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="engines" type="button">Power</button>
                      </div>
                    </div>
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{cards}</div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                """
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-[1.4fr,1fr]">
                    <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                      <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Representative Product Detail</div>
                      <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary">Sample Product Page Kept from the Strongest Detail Concept</h2>
                      <p class="mb-6 text-sm leading-relaxed text-on-surface-variant">
                        The final build keeps one product detail example so future product pages have a clear template. Technical figures remain neutral where the imported values could not be verified automatically.
                      </p>
                      <div class="flex flex-wrap gap-4">
                        <a class="inline-flex items-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-white hover:bg-primary-container" href="/products/viking-braidline-nylon-super-hawser.html">Open product detail</a>
                        <a class="inline-flex items-center rounded-md border border-primary px-5 py-3 text-sm font-bold text-primary hover:bg-primary hover:text-white" href="/inquiries/product-inquiry.html">Start product inquiry</a>
                      </div>
                    </div>
                    <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                      <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Placeholder Content</div>
                      <h3 class="mb-4 text-2xl font-extrabold">What still needs manual business input</h3>
                      <ul class="space-y-3 text-sm leading-relaxed text-on-primary-container">
                        <li>Product Description Placeholder</li>
                        <li>Compliance Information Placeholder</li>
                        <li>Approved supplier, stock, and lead-time details</li>
                        <li>Verified technical specification sheets</li>
                      </ul>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
            cta_band(
                "Need help finding the right category?",
                "The technical assistance and product inquiry routes are available if the catalog is not enough on its own.",
                "Product Inquiry",
                "/inquiries/product-inquiry.html",
                "Technical Assistance",
                SERVICE_DATA["technical-assistance"].path,
            ),
        ]
    )
    return render_page("Products | Marine Consultants", "Single approved product catalog for the final consolidated Marine Consultants build.", "products", body)


def render_services() -> str:
    cards = "".join(service_card(SERVICE_DATA[slug]) for slug in SERVICE_ORDER)
    body = "\n".join(
        [
            hero(
                "Regional service support",
                "Marine Service Capabilities",
                "The final services page consolidates the strongest Stitch support concepts into one maintainable overview with clear routes for inspections, maintenance, certification support, servicing, procurement, and assistance.",
                image_url=IMAGE_SERVICES,
                primary_href="/inquiries/service-inquiry.html",
                primary_label="Service Inquiry",
                secondary_href="/request-quote.html",
                secondary_label="Request a Quote",
                panel_title="Service Themes",
                panel_items=(
                    ("Inspection", "Condition and program support"),
                    ("Maintenance", "Planned and corrective coordination"),
                    ("Procurement", "Technical sourcing and follow-up"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Services", "One Approved Service Overview", "Duplicate service hubs and support portals have been replaced with one canonical overview plus dedicated subpages for each service type.")}
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{cards}</div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                """
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    <div class="grid gap-6 lg:grid-cols-3">
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
                        <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Step 1</div>
                        <h3 class="mb-3 text-xl font-bold text-primary">Define the support need</h3>
                        <p class="text-sm leading-relaxed text-on-surface-variant">Identify whether the request is inspection, maintenance, servicing, certification support, procurement, or open technical assistance.</p>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
                        <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Step 2</div>
                        <h3 class="mb-3 text-xl font-bold text-primary">Share the vessel or project context</h3>
                        <p class="text-sm leading-relaxed text-on-surface-variant">Use the service inquiry path to share scope, timing, and any supporting documents required for triage.</p>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
                        <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Step 3</div>
                        <h3 class="mb-3 text-xl font-bold text-primary">Move into quote or follow-up</h3>
                        <p class="text-sm leading-relaxed text-on-surface-variant">Once the scope is clear, the site routes the request into the quote page or a direct follow-up conversation.</p>
                      </div>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
            cta_band(
                "Need open-ended support instead of a fixed quote?",
                "Use the support request route when the scope is still evolving and needs triage before quoting.",
                "Support Request",
                SERVICE_DATA["support-request"].path,
                "Contact Page",
                "/contact.html",
            ),
        ]
    )
    return render_page("Services | Marine Consultants", "Canonical services overview for the final consolidated Marine Consultants website.", "services", body)


def render_resources() -> str:
    resource_cards = "".join(
        dedent(
            f"""
            <article class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
              <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">{escape(group)}</div>
              <h3 class="mb-3 text-2xl font-bold text-primary">{escape(title)}</h3>
              <p class="mb-6 text-sm leading-relaxed text-on-surface-variant">{escape(copy)}</p>
              <button class="rounded-md bg-primary px-5 py-3 text-sm font-bold text-white hover:bg-primary-container" data-toast-body="This document slot is present in the final build and ready for approved file uploads." data-toast-title="{escape(title)}" type="button">Document placeholder</button>
            </article>
            """
        ).strip()
        for title, copy, group in RESOURCE_ITEMS
    )
    body = "\n".join(
        [
            hero(
                "Catalogue and resources",
                "Catalogue / Resources",
                "The final resources page replaces mixed technical-spec, support, and catalog variants with one approved route for documents, downloadable assets, and placeholder business materials.",
                image_url=IMAGE_RESOURCES,
                primary_href="/products.html",
                primary_label="Browse Products",
                secondary_href="/news.html",
                secondary_label="View Updates",
                panel_title="Resources Status",
                panel_items=(
                    ("Catalog", "Catalogue Download Placeholder"),
                    ("Compliance", "Compliance Information Placeholder"),
                    ("Profile", "Company Overview Placeholder"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Resources", "Approved Placeholder Library", "The exported resource concepts contained repeated catalog and technical-sheet concepts with varying wording. They are now consolidated here as one editable document hub.")}
                    <div class="grid gap-6 md:grid-cols-2">{resource_cards}</div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                """
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-2">
                    <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                      <h3 class="mb-4 text-2xl font-bold text-primary">Manual input still required</h3>
                      <ul class="space-y-3 text-sm leading-relaxed text-on-surface-variant">
                        <li>Catalogue Download Placeholder</li>
                        <li>Compliance Information Placeholder</li>
                        <li>Company Overview Placeholder</li>
                        <li>Approved file names, versions, and publication dates</li>
                      </ul>
                    </div>
                    <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                      <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Editorial note</div>
                      <p class="text-sm leading-relaxed text-on-primary-container">
                        The previous Stitch passes mixed resources with support hubs, catalog pages, and download buttons that had no backed files. The final build keeps the UI and action points while making those empty states explicit.
                      </p>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page("Resources | Marine Consultants", "Canonical catalogue and resources page for the final consolidated Marine Consultants site.", "resources", body)


def render_news() -> str:
    news_cards = "".join(
        dedent(
            f"""
            <article class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft" data-filter-item="{escape(title + ' ' + copy + ' ' + group)}" data-filter-groups="{escape(group.lower())}">
              <div class="mb-4 flex items-center justify-between gap-4">
                <span class="rounded-full bg-surface-container px-3 py-1 text-[11px] font-bold uppercase tracking-[0.16em] text-secondary">{escape(group)}</span>
                <span class="text-xs font-semibold uppercase tracking-[0.16em] text-outline">Date Placeholder</span>
              </div>
              <h3 class="mb-3 text-2xl font-bold text-primary">{escape(title)}</h3>
              <p class="mb-6 text-sm leading-relaxed text-on-surface-variant">{escape(copy)}</p>
              <a class="text-sm font-bold text-on-tertiary-container hover:text-primary" href="/resources.html">View related resources</a>
            </article>
            """
        ).strip()
        for title, copy, group in NEWS_ITEMS
    )
    body = "\n".join(
        [
            hero(
                "News and updates",
                "Regional News / Updates",
                "The final news page keeps the visual hierarchy of the strongest Stitch news layout while removing unsupported achievements, percentages, facility milestones, and invented dates.",
                image_url=IMAGE_NEWS,
                primary_href="/resources.html",
                primary_label="Open Resources",
                secondary_href="/contact.html",
                secondary_label="Contact the Team",
                panel_title="Publishing Note",
                panel_items=(
                    ("Status", "Placeholder archive"),
                    ("Scope", "Approved business updates only"),
                    ("Next Step", "Replace cards with verified notices"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl" data-filter-root>
                    {section_intro("Updates", "Placeholder News Archive", "No verified newsroom dataset came with the export, so the live page now uses explicit placeholder cards instead of pretending unsupported milestones are real.")}
                    <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <input class="w-full rounded-xl border-none bg-surface-container-low px-5 py-4 text-sm text-on-surface shadow-soft focus:ring-2 focus:ring-primary-container lg:max-w-md" data-filter-search placeholder="Search placeholder updates..." type="search" />
                      <div class="flex flex-wrap gap-3">
                        <button class="filter-chip-active rounded-full border border-primary px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="all" type="button">All</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="operations" type="button">Operations</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="products" type="button">Products</button>
                        <button class="rounded-full border border-outline-variant px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]" data-filter-button="service" type="button">Service</button>
                      </div>
                    </div>
                    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{news_cards}</div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page("News | Marine Consultants", "Canonical placeholder news and updates page for the final consolidated Marine Consultants site.", "news", body)


def render_contact() -> str:
    placeholders = "".join(
        dedent(
            f"""
            <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-7 shadow-soft">
              <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-surface-container text-primary">
                <span class="material-symbols-outlined text-2xl">{icon}</span>
              </div>
              <h3 class="mb-3 text-xl font-bold text-primary">{title}</h3>
              <p class="text-sm leading-relaxed text-on-surface-variant">{copy}</p>
            </div>
            """
        ).strip()
        for title, copy, icon in (
            ("Regional Base", "Contact Details Placeholder", "location_on"),
            ("Commercial Email", "Contact Details Placeholder", "mail"),
            ("Telephone", "Contact Details Placeholder", "call"),
        )
    )
    body = "\n".join(
        [
            hero(
                "Regional contact route",
                "Contact Marine Consultants",
                "The contact page now uses simple regional framing, explicit placeholders for unverified details, and clean links into general, product, service, and quote inquiries.",
                image_url=IMAGE_CONTACT,
                primary_href="/inquiries/product-inquiry.html",
                primary_label="Product Inquiry",
                secondary_href="/inquiries/service-inquiry.html",
                secondary_label="Service Inquiry",
                panel_title="Contact Notes",
                panel_items=(
                    ("Region", "Trinidad & Tobago / Caribbean"),
                    ("Details", "Contact Details Placeholder"),
                    ("Quote Route", "Request a Quote page"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl">
                    {section_intro("Contact", "Editable Contact Details", "The exported contact variants included invented phone numbers, emails, and office listings. The final page keeps the layout but marks those items as placeholders until the business confirms them.")}
                    <div class="grid gap-6 md:grid-cols-3">{placeholders}</div>
                  </div>
                </section>
                """
            ).strip(),
            inquiry_form(
                title="General Inquiry",
                intro="Use the general inquiry form when the request does not fit neatly into product or service routing.",
                success_title="General inquiry captured",
                success_body="This local build confirms the form behavior and leaves final delivery routing ready for backend integration.",
                category_options=("General Contact", "Product Inquiry", "Service Inquiry", "Request a Quote"),
            ),
            support_paths(),
        ]
    )
    return render_page("Contact | Marine Consultants", "Canonical contact page for the final consolidated Marine Consultants site.", "contact", body)


def render_request_quote() -> str:
    body = "\n".join(
        [
            hero(
                "Consolidated quote route",
                "Request a Quote",
                "This is the single approved quote page for products, services, technical procurement, and bundled support requests.",
                image_url=IMAGE_QUOTE,
                primary_href="/inquiries/product-inquiry.html",
                primary_label="Product Inquiry",
                secondary_href="/inquiries/service-inquiry.html",
                secondary_label="Service Inquiry",
                panel_title="Quote Intake",
                panel_items=(
                    ("Route", "One canonical quote page"),
                    ("Support", "Product and service follow-up"),
                    ("Data", "Manual commercial details pending"),
                ),
            ),
            inquiry_form(
                title="Quote Request Form",
                intro="Use this form for commercial quotations, bundled service requests, or technical procurement questions that are ready for pricing review.",
                success_title="Quote request captured",
                success_body="The final quote route is functioning locally and ready for backend or CRM integration when approved.",
                category_options=("Marine Products", "Inspection Services", "Maintenance Support", "Certification Support", "Procurement / Supply Support", "Technical Assistance"),
            ),
        ]
    )
    return render_page("Request a Quote | Marine Consultants", "Canonical request-a-quote page for the final consolidated Marine Consultants site.", "contact", body)


def render_about_subpage(title: str, hero_title: str, intro_copy: str, main_heading: str, main_copy: str, secondary_heading: str, secondary_copy: str) -> str:
    body = "\n".join(
        [
            hero(
                "About subpage",
                hero_title,
                intro_copy,
                image_url=IMAGE_ABOUT,
                primary_href="/about.html",
                primary_label="Back to About",
                secondary_href="/contact.html",
                secondary_label="Contact the Team",
                panel_title="Subpage Focus",
                panel_items=(
                    ("Section", hero_title),
                    ("Status", "Approved canonical route"),
                    ("Input", "Manual business content ready"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-2">
                    <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                      <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary">{escape(main_heading)}</h2>
                      <p class="text-sm leading-relaxed text-on-surface-variant">{escape(main_copy)}</p>
                    </div>
                    <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                      <h2 class="mb-4 text-3xl font-extrabold tracking-tight">{escape(secondary_heading)}</h2>
                      <p class="text-sm leading-relaxed text-on-primary-container">{escape(secondary_copy)}</p>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page(title, f"{title} page for the final consolidated Marine Consultants site.", "about", body)


def render_category_page(category: Category) -> str:
    related = "".join(
        f'<a class="inline-flex rounded-full border border-outline-variant px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="{escape(CATEGORY_DATA[slug].path)}">{escape(CATEGORY_DATA[slug].title)}</a>'
        for slug in category.related
        if slug in CATEGORY_DATA
    )
    if category.slug == "chains-ropes-rigging":
        related += '<a class="inline-flex rounded-full border border-outline-variant px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="/products/viking-braidline-nylon-super-hawser.html">Representative product detail</a>'

    body = "\n".join(
        [
            hero(
                "Product category",
                category.title,
                category.summary,
                image_url=IMAGE_PRODUCTS,
                primary_href="/request-quote.html",
                primary_label="Request a Quote",
                secondary_href="/inquiries/product-inquiry.html",
                secondary_label="Product Inquiry",
                panel_title="Category Template",
                panel_items=(
                    ("Overview", "Short category summary"),
                    ("Groups", f"{len(category.groups)} product groups"),
                    ("Status", "Ready for manual enrichment"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
                    <div class="space-y-6">
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                        <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary">Category Overview</h2>
                        <p class="text-sm leading-relaxed text-on-surface-variant">{escape(category.overview)}</p>
                      </div>
                      {grid_block("Product Groups / Subcategories", category.groups, "check_circle")}
                      {grid_block("Representative Products", category.representative_products, "inventory_2")}
                    </div>
                    <div class="space-y-6">
                      <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                        <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-on-tertiary-container">Supporting Image Area</div>
                        <div class="flex aspect-[4/3] items-center justify-center rounded-2xl border border-white/10 bg-white/5">
                          <div class="text-center">
                            <span class="material-symbols-outlined text-6xl text-on-tertiary-container">{escape(category.icon)}</span>
                            <div class="mt-3 text-sm font-semibold text-on-primary-container">{escape(category.title)}</div>
                          </div>
                        </div>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                        <h3 class="mb-4 text-2xl font-bold text-primary">Related Categories</h3>
                        <div class="flex flex-wrap gap-3">{related}</div>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-low p-8 shadow-soft">
                        <h3 class="mb-4 text-2xl font-bold text-primary">Manual content still needed</h3>
                        <ul class="space-y-3 text-sm leading-relaxed text-on-surface-variant">
                          <li>Product Description Placeholder</li>
                          <li>Compliance Information Placeholder</li>
                          <li>Approved brands, models, and supplier references</li>
                          <li>Verified technical specification sheets</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page(f"{category.title} | Marine Consultants", f"{category.title} category page for the final consolidated Marine Consultants site.", "products", body)


def render_service_page(service: Service) -> str:
    related = "".join(
        f'<a class="inline-flex rounded-full border border-outline-variant px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="{escape(SERVICE_DATA[slug].path)}">{escape(SERVICE_DATA[slug].title)}</a>'
        for slug in service.related
    )
    body = "\n".join(
        [
            hero(
                "Service route",
                service.title,
                service.summary,
                image_url=IMAGE_SERVICES,
                primary_href="/inquiries/service-inquiry.html",
                primary_label="Service Inquiry",
                secondary_href="/request-quote.html",
                secondary_label="Request a Quote",
                panel_title="Service Template",
                panel_items=(
                    ("Overview", "Concise support summary"),
                    ("Audience", f"{len(service.audience)} audience groups"),
                    ("Status", "Ready for approved detail updates"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
                    <div class="space-y-6">
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                        <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary">Service Overview</h2>
                        <p class="text-sm leading-relaxed text-on-surface-variant">{escape(service.overview)}</p>
                      </div>
                      {grid_block("Scope of Support", service.scope, "construction")}
                      {grid_block("Who It Is For", service.audience, "groups")}
                    </div>
                    <div class="space-y-6">
                      <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                        <h3 class="mb-4 text-2xl font-bold">Related Services</h3>
                        <div class="flex flex-wrap gap-3">{related}</div>
                      </div>
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-low p-8 shadow-soft">
                        <h3 class="mb-4 text-2xl font-bold text-primary">Manual content still needed</h3>
                        <ul class="space-y-3 text-sm leading-relaxed text-on-surface-variant">
                          <li>Service Description Placeholder</li>
                          <li>Compliance Information Placeholder</li>
                          <li>Confirmed service coverage and scheduling notes</li>
                          <li>Approved supporting documents or service reports</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page(f"{service.title} | Marine Consultants", f"{service.title} page for the final consolidated Marine Consultants website.", "services", body)


def render_product_detail() -> str:
    body = "\n".join(
        [
            hero(
                "Representative product detail",
                "Viking Braidline Nylon Super Hawser",
                "This detail page is kept as the final product-template example from the strongest Stitch pass, but the technical values remain neutral until manually verified.",
                image_url=IMAGE_PRODUCT_DETAIL,
                primary_href="/request-quote.html",
                primary_label="Request a Quote",
                secondary_href="/categories/chains-ropes-rigging.html",
                secondary_label="Back to Rigging",
                panel_title="Product Template",
                panel_items=(
                    ("Category", "Chains, Ropes & Rigging"),
                    ("Specs", "Sizes / Variants Placeholder"),
                    ("Status", "Representative detail page"),
                ),
            ),
            dedent(
                f"""
                <section class="bg-surface px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 lg:grid-cols-[1fr,1.05fr]">
                    <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                      <div class="aspect-square overflow-hidden rounded-2xl bg-surface-container"><img alt="Representative rope product" class="h-full w-full object-cover" src="{escape(IMAGE_PRODUCT_DETAIL)}" /></div>
                    </div>
                    <div class="space-y-6">
                      <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                        <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-primary">Product Summary</h2>
                        <p class="text-sm leading-relaxed text-on-surface-variant">
                          Product Summary Placeholder. The Stitch source contained a plausible detail concept, but the numerical tables and approval references were not independently verified in this cleanup pass.
                        </p>
                      </div>
                      {grid_block("Key Features", ("High-visibility product template", "Suitable for quote routing", "Can be extended with verified technical data", "Supports related-product linking"), "check_circle")}
                      {grid_block("Sizes / Variants", ("Sizes / Variants Placeholder", "Technical specification sheet placeholder", "Approved data to be inserted manually"), "straighten")}
                      {grid_block("Applications", ("Mooring and deck support planning", "Procurement comparison workflows", "Regional marine operations"), "settings")}
                    </div>
                  </div>
                </section>
                """
            ).strip(),
            dedent(
                """
                <section class="bg-surface-container-low px-6 py-24">
                  <div class="mx-auto max-w-7xl grid gap-6 md:grid-cols-2">
                    <div class="rounded-2xl border border-outline-variant/40 bg-surface-container-lowest p-8 shadow-soft">
                      <h3 class="mb-4 text-2xl font-bold text-primary">Related Products</h3>
                      <div class="flex flex-wrap gap-3">
                        <a class="inline-flex rounded-full border border-outline-variant px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="/categories/chains-ropes-rigging.html">Chains, Ropes & Rigging</a>
                        <a class="inline-flex rounded-full border border-outline-variant px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-container-low" href="/categories/engines-marine-power-systems.html">Engines / Marine Power Systems</a>
                      </div>
                    </div>
                    <div class="rounded-2xl border border-outline-variant/40 bg-primary p-8 text-white shadow-hero">
                      <h3 class="mb-4 text-2xl font-bold">Final verification note</h3>
                      <p class="text-sm leading-relaxed text-on-primary-container">
                        Replace placeholder specifications, part references, and approvals only after supplier documentation is confirmed. This keeps the final production build free of invented technical data.
                      </p>
                    </div>
                  </div>
                </section>
                """
            ).strip(),
        ]
    )
    return render_page("Viking Braidline Nylon Super Hawser | Marine Consultants", "Representative product detail page for the final consolidated Marine Consultants site.", "products", body)


def render_product_inquiry() -> str:
    body = "\n".join(
        [
            hero(
                "Product inquiry route",
                "Product Inquiry",
                "Use the product inquiry page when you already know the category, product family, or technical procurement need and do not want to start with a general contact form.",
                image_url=IMAGE_PRODUCTS,
                primary_href="/products.html",
                primary_label="Browse Products",
                secondary_href="/request-quote.html",
                secondary_label="Request a Quote",
                panel_title="Inquiry Path",
                panel_items=(
                    ("Type", "Product-focused"),
                    ("Flow", "Category > inquiry > quote"),
                    ("Status", "Ready for CRM or email integration"),
                ),
            ),
            inquiry_form(
                title="Product Inquiry Form",
                intro="Use this form to share product categories, vessel context, and sourcing requirements.",
                success_title="Product inquiry captured",
                success_body="The product inquiry flow is wired and ready for backend handoff once final contact details are confirmed.",
                category_options=tuple(CATEGORY_DATA[slug].title for slug in PRODUCT_CATEGORY_ORDER),
            ),
        ]
    )
    return render_page("Product Inquiry | Marine Consultants", "Canonical product inquiry page for the final consolidated Marine Consultants site.", "contact", body)


def render_service_inquiry() -> str:
    body = "\n".join(
        [
            hero(
                "Service inquiry route",
                "Service Inquiry",
                "Use the service inquiry page for inspections, maintenance support, servicing, certification support, or open technical requests that need triage before quoting.",
                image_url=IMAGE_SERVICES,
                primary_href="/services.html",
                primary_label="Browse Services",
                secondary_href="/request-quote.html",
                secondary_label="Request a Quote",
                panel_title="Inquiry Path",
                panel_items=(
                    ("Type", "Service-focused"),
                    ("Flow", "Service page > inquiry > quote"),
                    ("Status", "Ready for workflow integration"),
                ),
            ),
            inquiry_form(
                title="Service Inquiry Form",
                intro="Use this form to share the service type, vessel context, and support timeline needed for triage.",
                success_title="Service inquiry captured",
                success_body="The service inquiry flow is functioning locally and ready for backend routing.",
                category_options=tuple(SERVICE_DATA[slug].title for slug in SERVICE_ORDER),
            ),
        ]
    )
    return render_page("Service Inquiry | Marine Consultants", "Canonical service inquiry page for the final consolidated Marine Consultants site.", "contact", body)


def render_legal_page(title: str, headline: str, copy: str) -> str:
    body = dedent(
        f"""
        <section class="bg-surface px-6 py-28">
          <div class="mx-auto max-w-4xl rounded-3xl border border-outline-variant/40 bg-surface-container-lowest p-10 shadow-soft">
            <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">Placeholder Legal Page</div>
            <h1 class="mb-5 text-4xl font-extrabold tracking-tight text-primary">{escape(headline)}</h1>
            <p class="text-base leading-relaxed text-on-surface-variant">{escape(copy)}</p>
          </div>
        </section>
        """
    ).strip()
    return render_page(title, copy, "contact", body)


def render_not_found() -> str:
    body = dedent(
        """
        <section class="bg-surface px-6 py-28">
          <div class="mx-auto max-w-4xl rounded-3xl border border-outline-variant/40 bg-surface-container-lowest p-10 shadow-soft">
            <div class="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-secondary">404</div>
            <h1 class="mb-5 text-4xl font-extrabold tracking-tight text-primary">Page Not Found</h1>
            <p class="mb-8 text-base leading-relaxed text-on-surface-variant">This route is not part of the final approved page structure. Use the links below to return to the consolidated website.</p>
            <div class="flex flex-wrap gap-4">
              <a class="inline-flex items-center rounded-md bg-primary px-5 py-3 text-sm font-bold text-white hover:bg-primary-container" href="/index.html">Return Home</a>
              <a class="inline-flex items-center rounded-md border border-primary px-5 py-3 text-sm font-bold text-primary hover:bg-primary hover:text-white" href="/contact.html">Contact the Team</a>
            </div>
          </div>
        </section>
        """
    ).strip()
    return render_page("404 | Marine Consultants", "Fallback page for unknown routes.", "contact", body)


def write_text(destination: Path, content: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    print(f"Wrote {destination.relative_to(ROOT)}")


def write_favicon(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    width = height = 16
    blue = (0x28, 0x16, 0x00, 0xFF)
    orange = (0x00, 0x6A, 0xEB, 0xFF)
    white = (0xFF, 0xFF, 0xFF, 0xFF)

    pixels = bytearray()
    for y in range(height - 1, -1, -1):
        for x in range(width):
            color = blue if x < 8 else orange
            if 3 <= x <= 12 and 3 <= y <= 12 and abs(x - y) <= 1:
                color = white
            pixels.extend(color)

    mask = b"\x00\x00\x00\x00" * height
    dib_header = struct.pack("<IIIHHIIIIII", 40, width, height * 2, 1, 32, 0, len(pixels) + len(mask), 0, 0, 0, 0)
    image_data = dib_header + pixels + mask
    icon_header = struct.pack("<HHH", 0, 1, 1)
    directory_entry = struct.pack("<BBBBHHII", width, height, 0, 0, 1, 32, len(image_data), 22)
    destination.write_bytes(icon_header + directory_entry + image_data)
    print(f"Wrote {destination.relative_to(ROOT)}")


def clean_generated_output() -> None:
    for directory in (ROOT / "assets", ROOT / "about", ROOT / "categories", ROOT / "products", ROOT / "services", ROOT / "inquiries"):
        if directory.exists() and directory.is_dir():
            shutil.rmtree(directory)
    for stale_file in (ROOT / "support.html", ROOT / "industries.html", ROOT / "quote.html"):
        if stale_file.exists():
            stale_file.unlink()


def build_pages() -> dict[str, str]:
    pages = {
        "index.html": render_home(),
        "about.html": render_about(),
        "products.html": render_products(),
        "services.html": render_services(),
        "resources.html": render_resources(),
        "news.html": render_news(),
        "contact.html": render_contact(),
        "request-quote.html": render_request_quote(),
        "about/company-overview.html": render_about_subpage(
            "Company Overview | Marine Consultants",
            "Company Overview",
            "This page holds the approved company profile route for verified business background, ownership context, and operating scope.",
            "Company Overview Placeholder",
            "Use this page to add the verified company profile once the business confirms history, ownership, operating scope, and regional footprint details.",
            "Why this is now separate",
            "The imported Stitch passes blended company overview copy into multiple about variants. The final build keeps one dedicated overview route to avoid conflicting versions.",
        ),
        "about/quality-compliance.html": render_about_subpage(
            "Quality / Compliance | Marine Consultants",
            "Quality / Compliance",
            "This page is reserved for approved quality, audit, compliance, and approval information once it is verified by the business.",
            "Compliance Information Placeholder",
            "Add only confirmed approvals, audit programs, quality systems, and partner or authority references here. Unsupported claims have been intentionally removed from the final build.",
            "What was removed",
            "The duplicate Stitch variants contained unsupported dates, certifications, and authority claims. The final page keeps the structure without asserting anything unverified.",
        ),
        "about/leadership.html": render_about_subpage(
            "Leadership | Marine Consultants",
            "Leadership / Team",
            "This page is reserved for approved leadership names, roles, biographies, and team structure.",
            "Leadership Placeholder",
            "Insert approved leadership names, titles, professional summaries, and team imagery once the business confirms them for publication.",
            "Why placeholders remain",
            "The export included invented or unsupported executive framing. The final build keeps a clean leadership route but does not invent names, counts, or credentials.",
        ),
        "products/viking-braidline-nylon-super-hawser.html": render_product_detail(),
        "inquiries/product-inquiry.html": render_product_inquiry(),
        "inquiries/service-inquiry.html": render_service_inquiry(),
        "privacy.html": render_legal_page("Privacy | Marine Consultants", "Privacy Policy Placeholder", "The Stitch export did not include approved privacy-policy content. Add the final legal copy here before public launch."),
        "terms.html": render_legal_page("Terms | Marine Consultants", "Terms Placeholder", "The Stitch export did not include approved terms content. Add the final legal copy here before public launch."),
        "404.html": render_not_found(),
    }
    for slug in PRODUCT_CATEGORY_ORDER:
        pages[CATEGORY_DATA[slug].path.lstrip("/")] = render_category_page(CATEGORY_DATA[slug])
    for slug in SERVICE_ORDER:
        pages[SERVICE_DATA[slug].path.lstrip("/")] = render_service_page(SERVICE_DATA[slug])
    return pages


def main() -> None:
    clean_generated_output()
    pages = build_pages()
    write_text(ASSETS_DIR / "site.css", SITE_CSS + "\n")
    write_text(ASSETS_DIR / "site.js", SITE_JS + "\n")
    for relative_path, content in pages.items():
        write_text(ROOT / relative_path, content)
    write_text(ROOT / "vercel.json", VERCEL_CONFIG)
    write_favicon(ROOT / "favicon.ico")
    print(f"Generated {len(pages)} pages and shared assets.")


if __name__ == "__main__":
    main()
