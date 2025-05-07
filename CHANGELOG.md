# CHANGELOG


## v2.1.1 (2025-05-07)

### Refactoring

- Rename display_layer_path to segmentation_ann_path and sort map dict
  ([`584ec55`](https://github.com/OpenPecha/toolkit-v2/commit/584ec552ee838068f4de5c48210b16b1230459f5))

- Simplify mapping functions and improve variable naming clarity
  ([`ae2a07d`](https://github.com/OpenPecha/toolkit-v2/commit/ae2a07d205916f6718ae7c77591ed66a7da2bd41))


## v2.1.0 (2025-05-04)

### Bug Fixes

- Annotation offset edits in update layer
  ([`3c7d535`](https://github.com/OpenPecha/toolkit-v2/commit/3c7d5350c85170907e8bca9f2e96a6dcd8e8a063))

- Update layer
  ([`dcbc1f8`](https://github.com/OpenPecha/toolkit-v2/commit/dcbc1f8e322be658760119d784436f6e8776ae11))

- **pecha.merge**: Update reference resources
  ([`be29654`](https://github.com/OpenPecha/toolkit-v2/commit/be296544ff485dd7bc1e92d78891303a3439be55))

### Features

- Implement docx annotation update functionality
  ([`05d9e51`](https://github.com/OpenPecha/toolkit-v2/commit/05d9e514abfbfbea175feb8d1157f3b73251d9ce))

- Import blupdate from old version
  ([`b671460`](https://github.com/OpenPecha/toolkit-v2/commit/b6714609d0eea1a2f302551e257a37cda621b73c))

- Load annotation store as layer
  ([`9e3e11e`](https://github.com/OpenPecha/toolkit-v2/commit/9e3e11e7e599a40a3044a8c28146ddf6e9c1892d))

### Refactoring

- Move test data to SharedPechaSetup class
  ([`b82ae24`](https://github.com/OpenPecha/toolkit-v2/commit/b82ae24a2998fbd064c17979104306fe55f1c15b))

- Remove language-specific segment layer enums and use root_segment
  ([`9006439`](https://github.com/OpenPecha/toolkit-v2/commit/900643976cbf1193ff5480d0cfe303b78e2fa9e4))

- Rename meaning_segment_layer to layer for consistency
  ([`59723e6`](https://github.com/OpenPecha/toolkit-v2/commit/59723e6626d1231e55e868a5b327b9dccb252b14))

- Replace root_display_pecha with root_alignment_id in serializer
  ([`a82d243`](https://github.com/OpenPecha/toolkit-v2/commit/a82d243d89fb4506f0ddd21e5c6362a1a776b23c))

- Simplify test metadata using class attributes
  ([`cc24b40`](https://github.com/OpenPecha/toolkit-v2/commit/cc24b409c2f20dfb4e81499922753e6b9852188b))

- Update LayerEnum values to use uppercase constants
  ([`6174155`](https://github.com/OpenPecha/toolkit-v2/commit/61741552afbbc719e69e91aa9a300ce028f919b6))
