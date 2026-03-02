import { db } from '$lib/server/db';
import { postsTable } from '$lib/server/db/schema';
import { and, eq } from 'drizzle-orm';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
	const [post] = await db
		.select({
			id: postsTable.id,
			title: postsTable.title,
			body: postsTable.body,
			when_created: postsTable.when_created
		})
		.from(postsTable)
		.where(and(eq(postsTable.id, parseInt(params.post_id))));

	return { post };
};
