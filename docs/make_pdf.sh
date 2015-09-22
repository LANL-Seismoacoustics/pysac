#!/bin/bash

pandoc -f markdown -t latex --toc -o source/manual.pdf source/index.md source/package.md source/obspy.md source/license.md source/metadata.yaml
