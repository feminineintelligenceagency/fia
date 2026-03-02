import { API_KEY_COOKIE } from '$lib/consts';
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ cookies }) => {
	// make sure the user has an api key in cookies
	const key = cookies.get(API_KEY_COOKIE);

	if (!key) {
		redirect(307, '/');
	}

	return {};
};
