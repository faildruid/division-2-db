import { screen, render } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

test("End to end path test", async () => {
  localStorage.clear();
  render(<App />);
  const copyrightText = await screen.findByText(/copyright/i);
  expect(copyrightText).toBeInTheDocument();
})
