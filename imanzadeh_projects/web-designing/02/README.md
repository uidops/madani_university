# Persian Shop Demo

RTL Persian shop demo for the web-designing coursework.

## Files

| File | Description |
| --- | --- |
| `index.html` | Page structure for the product list, cart, modal, and controls. |
| `style.css` | RTL layout, product cards, cart styling, modal, toast, and responsive rules. |
| `script.js` | Product loading, pagination, cart behavior, discount handling, modal logic, and local storage. |
| `products.json` | Product data used by the page. |

## Run

Because the page fetches `products.json`, serve it from a local static server instead of opening the HTML file directly.

From this directory:

```bash
python3 -m http.server
```

Then open:

```text
http://localhost:8000
```

## Features

- RTL Persian interface.
- Product pagination.
- Product details modal.
- Shopping cart stored in `localStorage`.
- Random discount-code notification.
- Basic click tracking with browser storage.

## Notes

- Product data can be edited in `products.json`.
- Browser storage can be cleared to reset cart, page, and click-tracking data.
