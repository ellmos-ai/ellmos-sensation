"""CLI entrypoint for ellmos-sensation."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .sensor_hub import SensationHub, SensationPermissions


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ellmos-sensation", description="Permission-gated device perception CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show SensationHub permission and sensor status")

    pres_p = sub.add_parser("presence", help="Run zero-egress camera presence check")
    pres_p.add_argument("--allow-camera", action="store_true", help="Explicitly grant camera permission for this check")

    gate_p = sub.add_parser("open-compute-gate", help="Evaluate whether Open-Compute should pause")
    gate_p.add_argument("--allow-camera", action="store_true")
    gate_p.add_argument("--idle-seconds", type=float, default=0.0)

    args = parser.parse_args(argv)
    hub = SensationHub(SensationPermissions())

    if args.cmd == "status":
        print(json.dumps(hub.status(), indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "presence":
        hub.set_permissions(camera=bool(args.allow_camera))
        obs = hub.camera.check_presence(hub.permissions)
        print(json.dumps(obs.as_dict(), indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "open-compute-gate":
        hub.set_permissions(camera=bool(args.allow_camera))
        res = hub.open_compute_gate.evaluate(hub.permissions, idle_seconds=args.idle_seconds)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
