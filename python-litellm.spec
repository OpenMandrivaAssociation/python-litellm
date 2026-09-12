Name:		python-litellm
Version:	1.100.1
Release:	1
Summary:	Call 100+ LLM APIs with the OpenAI format
License:	MIT
Group:		Development/Python
URL:		https://github.com/BerriAI/litellm
Source0:	https://files.pythonhosted.org/packages/source/l/litellm/litellm-%{version}.tar.gz
BuildArch:	noarch
# METADATA pins floors/ceilings cooker will not match exactly
%global __requires_exclude ^python[0-9.]*dist\\(
BuildRequires:	python
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
Requires:	python%{pyver}dist(fastuuid)
Requires:	python%{pyver}dist(httpx)
Requires:	python%{pyver}dist(openai)
Requires:	python%{pyver}dist(python-dotenv)
Requires:	python%{pyver}dist(tiktoken)
Requires:	python%{pyver}dist(importlib-metadata)
Requires:	python%{pyver}dist(tokenizers)
Requires:	python%{pyver}dist(click)
Requires:	python%{pyver}dist(jinja2)
Requires:	python%{pyver}dist(aiohttp)
Requires:	python%{pyver}dist(pydantic)
Requires:	python%{pyver}dist(pydantic-settings)
Requires:	python%{pyver}dist(jsonschema)
Requires:	python%{pyver}dist(boto3)

%description
LiteLLM is a unified SDK for calling LLM providers with an
OpenAI-compatible interface. Aider uses it to talk to local
llama-server and Ollama as well as cloud APIs.

%prep
%autosetup -n litellm-%{version}
# sdist uses maturin for an optional 24MB rust bridge. Aider only
# needs the Python SDK; the loader already treats a missing _native
# as None. Build with setuptools so this stays noarch and offline.
sed -i \
	-e 's/requires = \["maturin==1.9.4"\]/requires = ["setuptools"]/' \
	-e 's/build-backend = "maturin"/build-backend = "setuptools.build_meta"/' \
	pyproject.toml
cat >> pyproject.toml << 'EOF'

[tool.setuptools.packages.find]
include = ["litellm", "litellm.*"]

[tool.setuptools.package-data]
"*" = ["*"]
EOF

%build

%install
python -m pip install \
	--no-deps --no-build-isolation --no-compile \
	--root %{buildroot} --prefix %{_prefix} \
	.
for cmd in litellm lite litellm-proxy; do
	if [ -f %{buildroot}%{_bindir}/$cmd ]; then
		sed -i '1s|^#!/usr/bin/env python3|#!/usr/bin/python|' \
			%{buildroot}%{_bindir}/$cmd
		sed -i '1s|^#!/usr/bin/python3|#!/usr/bin/python|' \
			%{buildroot}%{_bindir}/$cmd
	fi
done

%files
%doc README.md
%license LICENSE
%{_bindir}/litellm
%{_bindir}/lite
%{_bindir}/litellm-proxy
%{py_sitedir}/litellm
%{py_sitedir}/litellm-*.*-info
