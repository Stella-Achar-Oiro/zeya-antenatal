/**
 * Design tokens — single source of truth for all colours.
 * Import from here. Never hardcode hex values in components.
 */

export const colors = {
  /** Primary brand — buttons, active states, header backgrounds */
  sage: "#2D6A4F",
  sageDark: "#1B4332",
  sageLight: "#EEF7F2",
  sageLightMid: "#D8EDDF",

  /** Danger / emergency — used only for danger sign alerts */
  danger: "#B71C1C",
  dangerBg: "#FFEBEE",

  /** Warning — secondary alerts */
  amber: "#F57F17",
  amberBg: "#FFF8E1",

  /** Success / confirmation */
  green: "#2E7D32",
  greenBg: "#E8F5E9",

  /** Neutral */
  bg: "#FAFAFA",
  white: "#FFFFFF",
  divider: "#E5E5E5",
  gray: "#6B6B6B",
  mid: "#444444",
  dark: "#1A1A1A",

  /** Chat bubbles */
  userBubble: "#2D6A4F",
  userBubbleText: "#FFFFFF",
  assistantBubble: "#F0F4F0",
  assistantBubbleText: "#1A1A1A",
} as const;
