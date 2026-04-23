import { sql } from 'drizzle-orm';
import { bigint, integer, pgTable, serial, text, unique } from 'drizzle-orm/pg-core';

export const postsTable = pgTable('posts', {
	id: serial().primaryKey(),
	title: text().notNull(),
	body: text().notNull(),
	when_created: bigint({ mode: 'number' })
		.default(sql`EXTRACT(epoch FROM now())`)
		.notNull()
});

export const flavorsOfAbuseTable = pgTable('flavors_of_abuse', {
	id: serial().primaryKey(),
	name: text().notNull().unique()
});

export const traumasTable = pgTable('traumas', {
	id: serial().primaryKey(),
	name: text().notNull().unique(),
	abuse_techniques: text().notNull(),
	research_summary: text().notNull()
});

export const vulnerabilityTypesTable = pgTable('vulnerability_types', {
	id: serial().primaryKey(),
	name: text().notNull().unique(),
	vulnerability_traits: text().notNull(),
	abuse_techniques: text().notNull(),
	brain_biases: text().notNull()
});

export const playerTypologiesTable = pgTable('player_typologies', {
	id: serial().primaryKey(),
	name: text().notNull().unique(),
	alias: text().notNull(),
	summary: text().notNull(),
	main_motivation: text().notNull(),
	always_does_this: text().notNull(),
	he_never_does_this: text().notNull(),
	red_flags: text().notNull(),
	techniques_he_might_use: text().notNull(),
	vulnerability_traits: text().notNull()
});

export const playerToVulnerabilityTypesTable = pgTable(
	'player_to_vulnerability_types',
	{
		player_id: integer().references(() => playerTypologiesTable.id),
		vulnerability_type_id: integer().references(() => vulnerabilityTypesTable.id)
	},
	(t) => [unique().on(t.player_id, t.vulnerability_type_id)]
);

export const playerToTraumasTable = pgTable(
	'player_to_traumas',
	{
		player_id: integer().references(() => playerTypologiesTable.id),
		trauma_id: integer().references(() => traumasTable.id)
	},
	(t) => [unique().on(t.player_id, t.trauma_id)]
);

export const playerToFlavorsTable = pgTable(
	'player_to_flavors',
	{
		player_id: integer().references(() => playerTypologiesTable.id),
		flavor_id: integer().references(() => flavorsOfAbuseTable.id)
	},
	(t) => [unique().on(t.player_id, t.flavor_id)]
);

export const chatsTable = pgTable('chats', {
	id: text().primaryKey(),
	title: text().notNull(),
	when_created: bigint({ mode: 'number' })
		.default(sql`EXTRACT(epoch FROM now())`)
		.notNull()
});

export const chatMessagesTable = pgTable('chat_messages', {
	id: serial().primaryKey(),
	chat_id: text()
		.notNull()
		.references(() => chatsTable.id),
	role: text({ enum: ['user', 'assistant'] }).notNull(),
	content: text().notNull(),
	when_created: bigint({ mode: 'number' })
		.default(sql`EXTRACT(epoch FROM now())`)
		.notNull()
});
