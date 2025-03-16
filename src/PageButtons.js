import * as Inputs from "npm:@observablehq/inputs";
import { html } from "npm:htl";

export const PageButtons = (id, totalPages) => {
  return Inputs.button(
    [
      [html`<span id="${id}-first">⟪</span>`, () => 0],
      [html`<span id="${id}-prev">←</span>`, (page) => Math.max(0, page - 1)],
      [
        html`<span id="${id}-next">→</span>`,
        (page) => Math.min(totalPages - 1, page + 1),
      ],
      [html`<span id="${id}-last">⟫</span>`, () => totalPages - 1],
    ],
    { value: 0 }
  );
};
