import { test, expect } from "@playwright/test";

test("login page renders", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page.getByText("StayFlow Hotel Suite")).toBeVisible();
  await expect(page.getByRole("button", { name: "Login" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Sign up" })).toBeVisible();
});
