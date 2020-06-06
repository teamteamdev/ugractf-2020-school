{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    node
  ];

  pythonPackages = self: with self; [
    scapy
    gunicorn
    aiohttp
    aiohttp-jinja2
    pillow
    python-barcode
  ];
}
