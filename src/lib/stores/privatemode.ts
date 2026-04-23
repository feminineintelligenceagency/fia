import { writable } from 'svelte/store';

export type SessionResult = {
	id: string;
	title: string;
	source: string;
	createdAt: number;
	result: unknown;
};

export const privateMode = writable(false);
export const sessionResults = writable<SessionResult[]>([]);
export const activeResultId = writable<string | null>(null);

export function startPrivateMode() {
	privateMode.set(true);
	sessionResults.set([]);
	activeResultId.set(null);
}

export function stopPrivateMode() {
	privateMode.set(false);
	sessionResults.set([]);
	activeResultId.set(null);
}

export function addSessionResult(item: SessionResult) {
	sessionResults.update((arr) => [item, ...arr]);
	activeResultId.set(item.id);
}

export function setActiveResult(id: string) {
	activeResultId.set(id);
}

export function clearSession() {
	sessionResults.set([]);
	activeResultId.set(null);
}