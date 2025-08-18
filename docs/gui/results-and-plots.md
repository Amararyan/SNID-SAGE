## Results and Plots

After analysis:
- Summary shows type, best template, confidence, redshift, age
- Open dialogs for cluster summary, subtype proportions, redshift–age

Plots:
- Comparison (flux and flattened), redshift–age, 3D clustering (if available)

Export:
- Use File → Export or dialog Save/Export
- PNG for quick sharing; PDF/SVG for publications

CLI outputs:
- Standard: `{name}.output`, `{name}.fluxed`, `{name}.flattened`
- Complete adds plot files (`comparison`, `3d_gmm_clustering`, `redshift_age`, `cluster_subtypes`)

```powershell
sage data\sn2003jo.dat --output-dir results\ --complete
```

