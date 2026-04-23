import { db } from '$lib/server/db';
import { chatsTable } from '$lib/server/db/schema';
import { desc } from 'drizzle-orm';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ depends }) => {
	depends('chats');

	const chats = await db
		.select({
			id: chatsTable.id,
			title: chatsTable.title,
			when_created: chatsTable.when_created
		})
		.from(chatsTable)
		.orderBy(desc(chatsTable.when_created));

	return { chats };
};
