import type { RendererComponentType, UnsupportedComponentError } from "./types";

export type RendererRegistry<T> = Readonly<Record<RendererComponentType, T>>;

export type RendererResolution<T> =
  | Readonly<{ ok: true; renderer: T }>
  | Readonly<{ ok: false; error: UnsupportedComponentError }>;

export const createRendererRegistry = <T>(
  registry: RendererRegistry<T>,
): RendererRegistry<T> => Object.freeze({ ...registry });

export function resolveRenderer<T>(
  registry: RendererRegistry<T>,
  component: string,
): RendererResolution<T> {
  if (Object.prototype.hasOwnProperty.call(registry, component))
    return {
      ok: true,
      renderer: registry[component as RendererComponentType],
    };
  return {
    ok: false,
    error: {
      code: "UNSUPPORTED_COMPONENT",
      component,
      message: `This client cannot safely render assessment component ${component}.`,
    },
  };
}
