import { getTypologies, getAbuseFlavors } from '$lib/server/rag-api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const [typologies, abuseFlavors] = await Promise.all([getTypologies(), getAbuseFlavors()]);

	return {
		typologies: typologies ?? [],
		abuseFlavors: abuseFlavors ?? [],
		backendAvailable: typologies !== null
	};
};
