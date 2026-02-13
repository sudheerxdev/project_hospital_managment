export const ROLE_ALIASES = {
  patient: "guest",
  receptionist: "front_desk",
  doctor: "manager",
  nurse: "housekeeping",
};

export function normalizeRole(role) {
  return ROLE_ALIASES[role] || role;
}

export const ROUTE_PERMISSIONS = {
  "/dashboard": ["admin", "manager", "front_desk", "accountant", "housekeeping", "guest"],
  "/guests": ["admin", "manager", "front_desk"],
  "/bookings": ["admin", "manager", "front_desk"],
  "/services": ["admin", "manager", "front_desk", "housekeeping", "guest"],
  "/invoices": ["admin", "manager", "accountant", "front_desk", "guest"],
  "/notifications": ["admin", "manager", "front_desk"],
};

export function canAccess(role, path) {
  const normalized = normalizeRole(role);
  const allowed = ROUTE_PERMISSIONS[path];
  if (!allowed) return false;
  return allowed.includes(normalized);
}

export function firstAllowedRoute(role) {
  const normalized = normalizeRole(role);
  for (const [route, allowed] of Object.entries(ROUTE_PERMISSIONS)) {
    if (allowed.includes(normalized)) return route;
  }
  return "/dashboard";
}
