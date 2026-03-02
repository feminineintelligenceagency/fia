import { resolve } from '$app/paths';
import { API_KEY_COOKIE } from '$lib/consts';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	const key = cookies.get(API_KEY_COOKIE);
	if (key) {
		redirect(307, resolve('/app'));
	}

	return {};
};
