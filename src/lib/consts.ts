import { isHttpError } from '@sveltejs/kit';
import { toast } from 'svelte-sonner';

export function handleError(err: unknown) {
	if (isHttpError(err)) {
		toast.error(err.body.message);
	} else {
		toast.error('Unhandled error');
	}
}

export const API_KEY_COOKIE = 'Api-Key';

export function getTimestampInSeconds() {
	return Math.floor(Date.now() / 1000);
}

export const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
