import { db } from '$lib/server/db';
import {
	flavorsOfAbuseTable,
	playerToFlavorsTable,
	playerToTraumasTable,
	playerToVulnerabilityTypesTable,
	playerTypologiesTable,
	traumasTable,
	vulnerabilityTypesTable
} from '$lib/server/db/schema';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const players = await db
		.select({
			id: playerTypologiesTable.id,
			name: playerTypologiesTable.name,
			summary: playerTypologiesTable.summary,
			main_motivation: playerTypologiesTable.main_motivation,
			red_flags: playerTypologiesTable.red_flags,
			techniques_he_might_use: playerTypologiesTable.techniques_he_might_use
		})
		.from(playerTypologiesTable)
		.orderBy(playerTypologiesTable.id);

	const flavors = await db
		.select({
			id: flavorsOfAbuseTable.id,
			name: flavorsOfAbuseTable.name
		})
		.from(flavorsOfAbuseTable)
		.orderBy(flavorsOfAbuseTable.id);

	const playerToFlavors = await db.select().from(playerToFlavorsTable);

	const traumas = await db
		.select({
			id: traumasTable.id,
			name: traumasTable.name,
			abuse_techniques: traumasTable.abuse_techniques,
			research_summary: traumasTable.research_summary
		})
		.from(traumasTable)
		.orderBy(traumasTable.id);

	const playerToTraumas = await db.select().from(playerToTraumasTable);

	const vulnerabilities = await db
		.select({
			id: vulnerabilityTypesTable.id,
			name: vulnerabilityTypesTable.name,
			traits: vulnerabilityTypesTable.vulnerability_traits,
			abuse_techniques: vulnerabilityTypesTable.abuse_techniques,
			brain_biases: vulnerabilityTypesTable.brain_biases
		})
		.from(vulnerabilityTypesTable)
		.orderBy(vulnerabilityTypesTable.id);

	const playerToVulnerabilities = await db
		.select({
			player_id: playerToVulnerabilityTypesTable.player_id,
			vulnerability_id: playerToVulnerabilityTypesTable.vulnerability_type_id
		})
		.from(playerToVulnerabilityTypesTable);

	return {
		players,
		flavors,
		playerToFlavors,
		traumas,
		playerToTraumas,
		vulnerabilities,
		playerToVulnerabilities
	};
};
