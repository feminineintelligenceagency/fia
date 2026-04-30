import { db } from '$lib/server/db';
import { chatMessagesTable, chatsTable } from '$lib/server/db/schema';
import { error } from '@sveltejs/kit';
import { asc, eq } from 'drizzle-orm';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, depends }) => {
	depends('chat');

	const [chat] = await db
		.select({
			id: chatsTable.id,
			title: chatsTable.title
		})
		.from(chatsTable)
		.where(eq(chatsTable.id, params.chat_id));

	if (!chat) {
		error(404, 'Chat not found');
	}

	const messages = await db
		.select({
			id: chatMessagesTable.id,
			role: chatMessagesTable.role,
			content: chatMessagesTable.content,
			when_created: chatMessagesTable.when_created
		})
		.from(chatMessagesTable)
		.where(eq(chatMessagesTable.chat_id, chat.id))
		.orderBy(asc(chatMessagesTable.when_created));

	return { chat, messages };
};
