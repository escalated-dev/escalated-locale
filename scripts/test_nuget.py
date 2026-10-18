#!/usr/bin/env python3
"""Exercise the public .NET API from source and a fresh, unpublished NuGet package."""

import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT = REPO_ROOT / "packages/nuget/Escalated.Locale.csproj"
CONTRACTS = REPO_ROOT / "tests/nuget/Locale.Contracts.csproj"
AUDIT = ["-p:NuGetAuditMode=all", "-warnaserror:NU1900,NU1901,NU1902,NU1903,NU1904,NU1905"]


def run(*arguments, env=None):
    print("+ " + " ".join(str(value) for value in arguments), flush=True)
    subprocess.run([str(value) for value in arguments], cwd=REPO_ROOT, env=env, check=True)


def configuration(path, sources, *, map_package=False):
    config = ET.Element("configuration")
    package_sources = ET.SubElement(config, "packageSources")
    ET.SubElement(package_sources, "clear")
    for key, value in sources:
        ET.SubElement(package_sources, "add", key=key, value=str(value))
    if map_package:
        mapping = ET.SubElement(config, "packageSourceMapping")
        for key, pattern in [("local", "Escalated.Locale"), ("nuget.org", "*")]:
            source = ET.SubElement(mapping, "packageSource", key=key)
            ET.SubElement(source, "package", pattern=pattern)
    ET.ElementTree(config).write(path, encoding="utf-8", xml_declaration=True)


def main():
    sdk = subprocess.check_output(["dotnet", "--version"], cwd=REPO_ROOT, text=True).strip()
    if not sdk.startswith("8."):
        raise RuntimeError(f"Expected .NET SDK 8, got {sdk}")
    print(f"SDK: {sdk}", flush=True)

    with tempfile.TemporaryDirectory(prefix="escalated-locale-nuget-") as directory:
        temporary = Path(directory).resolve()
        if temporary.parent != Path(tempfile.gettempdir()).resolve():
            raise RuntimeError("Unexpected temporary directory location")
        public_config = temporary / "public.NuGet.Config"
        public_source = ("nuget.org", "https://api.nuget.org/v3/index.json")
        configuration(public_config, [public_source])
        run("dotnet", "restore", CONTRACTS, "--configfile", public_config, *AUDIT)
        run("dotnet", "run", "--project", CONTRACTS, "--configuration", "Release", "--no-restore")

        version = ET.parse(PROJECT).findtext("PropertyGroup/Version").split("-")[0]
        version += "-ci.r" + uuid.uuid4().hex[:12]
        feed = temporary / "feed"
        run("dotnet", "pack", PROJECT, "--configuration", "Release", "--no-build", "--no-restore",
            "--output", feed, f"-p:PackageVersion={version}")
        package = feed / f"Escalated.Locale.{version}.nupkg"
        if not package.is_file():
            raise RuntimeError("The build did not produce the expected NuGet package")
        with zipfile.ZipFile(package) as archive:
            if archive.read("README.md") != (PROJECT.parent / "README.md").read_bytes():
                raise RuntimeError("NuGet package is missing its current usage documentation")

        # Copy only the consumer and canonical JSON; no provider source or
        # project reference is available in this standalone installation.
        consumer_root = temporary / "consumer"
        consumer = consumer_root / "tests/nuget"
        consumer.mkdir(parents=True)
        for name in ["Locale.Contracts.csproj", "Program.cs"]:
            shutil.copy2(CONTRACTS.parent / name, consumer / name)
        shutil.copytree(REPO_ROOT / "locales", consumer_root / "locales")
        consumer_project = consumer / CONTRACTS.name
        package_config = temporary / "package.NuGet.Config"
        configuration(package_config, [("local", feed), public_source], map_package=True)
        cache = temporary / "package-cache"
        package_environment = dict(os.environ, NUGET_PACKAGES=str(cache))
        package_property = f"-p:LocalePackageVersion={version}"
        run("dotnet", "restore", consumer_project, package_property, "--configfile", package_config,
            *AUDIT, env=package_environment)

        assets = json.loads((consumer / "obj/project.assets.json").read_text(encoding="utf-8"))
        library = assets["libraries"][f"Escalated.Locale/{version}"]
        if library["type"] != "package" or any(value["type"] == "project" for value in assets["libraries"].values()):
            raise RuntimeError("The standalone consumer must use installed packages only")
        expected = base64.b64encode(hashlib.sha512(package.read_bytes()).digest()).decode("ascii")
        installed = cache / library["path"] / f"escalated.locale.{version}.nupkg.sha512"
        if installed.read_text(encoding="utf-8").strip() != expected:
            raise RuntimeError("Installed NuGet package differs from the artifact that was built")
        run("dotnet", "run", "--project", consumer_project, package_property,
            "--configuration", "Release", "--no-restore", env=package_environment)
        print(f"PACKAGED_LOCALE_OK: {version}; artifact SHA512 verified; fresh package-only consumer", flush=True)


if __name__ == "__main__":
    main()
