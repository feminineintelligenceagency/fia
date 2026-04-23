<script lang="ts">
	import playerTypologiesData from '$lib/data/player_typologies.json';
	import flavoursOfAbuseData from '$lib/data/flavours_of_abuse.json';
	import traumaData from '$lib/data/trauma.json';
	import vulnerabilityTypesData from '$lib/data/vulnerability_types.json';

	import ChevronLeft from '@lucide/svelte/icons/chevron-left';
	import ChevronRight from '@lucide/svelte/icons/chevron-right';
	import Search from '@lucide/svelte/icons/search';
	import X from '@lucide/svelte/icons/x';

	type PlayerTypology = {
		name: string;
		alias?: string;
		summary?: string | null;
		main_motivation?: string[] | null;
		vulnerability_types?: string[] | null;
		flavors_of_abuse?: string[] | null;
		always_does_this?: string[] | null;
		he_never_does_this?: string[] | null;
		red_flags?: string[] | null;
		techniques_he_might_use?: string[] | null;
		vulnerability_traits?: string[] | null;
		trauma_signs?: string[] | null;
		discovered_by?: string[] | null;
	};

	type AbuseFlavor = {
		Flavor: string;
		'Player typologies': string[];
	};

	type TraumaItem = {
		Name: string;
		'Player Typologies': string[] | null;
		'Abuse Techniques': string[] | null;
		'Research Summary': string | null;
	};

	type VulnerabilityType = {
		name: string;
		vulnerability_traits: string[] | null;
		abuse_techniques: string[] | null;
		brain_biases: string[] | null;
		flavors_of_abuse: string[] | null;
		player_typologies: string[] | null;
	};

	const playerTypologies = (playerTypologiesData.player_typologies as PlayerTypology[]).filter(
		(item) => item.name
	);

	const abuseFlavors = (flavoursOfAbuseData as AbuseFlavor[]).filter((item) => item.Flavor);

	const traumaItems = (traumaData as TraumaItem[]).filter((item) => item.Name);

	const vulnerabilityTypes = (vulnerabilityTypesData as VulnerabilityType[]).filter(
		(item) => item.name
	);

	let isOpen = $state(false);
	let activeTab = $state<'typologies' | 'flavors' | 'vulnerabilities' | 'trauma'>('typologies');
	let search = $state('');

	function normalize(value: string) {
		return value.toLowerCase().trim();
	}

	function matchesSearch(values: Array<string | null | undefined>) {
		if (!search.trim()) return true;
		const q = normalize(search);
		return values.some((value) => value && normalize(value).includes(q));
	}

	function cleanList(items?: string[] | null, count = 4) {
		if (!items) return [];
		return items.filter((item) => item && item !== 'No access').slice(0, count);
	}

	function getTypologyText(item: PlayerTypology) {
		return [
			item.name,
			item.alias,
			item.summary ?? '',
			...(item.main_motivation ?? []),
			...(item.flavors_of_abuse ?? []),
			...(item.vulnerability_types ?? []),
			...(item.red_flags ?? []),
			...(item.techniques_he_might_use ?? []),
			...(item.trauma_signs ?? [])
		];
	}

	function getFlavorText(item: AbuseFlavor) {
		return [item.Flavor, ...(item['Player typologies'] ?? [])];
	}

	function getVulnerabilityText(item: VulnerabilityType) {
		return [
			item.name,
			...(item.vulnerability_traits ?? []),
			...(item.abuse_techniques ?? []),
			...(item.brain_biases ?? []),
			...(item.flavors_of_abuse ?? []),
			...(item.player_typologies ?? [])
		];
	}

	function getTraumaText(item: TraumaItem) {
		return [
			item.Name,
			item['Research Summary'] ?? '',
			...(item['Player Typologies'] ?? []),
			...(item['Abuse Techniques'] ?? [])
		];
	}

	let filteredTypologies = $derived(
		playerTypologies.filter((item) => matchesSearch(getTypologyText(item))).slice(0, 20)
	);

	let filteredFlavors = $derived(
		abuseFlavors.filter((item) => matchesSearch(getFlavorText(item))).slice(0, 20)
	);

	let filteredVulnerabilities = $derived(
		vulnerabilityTypes.filter((item) => matchesSearch(getVulnerabilityText(item))).slice(0, 20)
	);

	let filteredTrauma = $derived(
		traumaItems.filter((item) => matchesSearch(getTraumaText(item))).slice(0, 20)
	);
</script>

<div class="fixed top-1/2 right-0 z-50 -translate-y-1/2">
	<button
		type="button"
		class="group flex items-center gap-2 rounded-l-2xl border border-slate-200 bg-white/95 px-3 py-3 text-slate-700 shadow-lg transition hover:bg-slate-50"
		onclick={() => (isOpen = !isOpen)}
	>
		{#if isOpen}
			<ChevronRight class="h-5 w-5" />
		{:else}
			<ChevronLeft class="h-5 w-5" />
		{/if}
		<span class="hidden text-xs font-semibold sm:block">Traits Panel</span>
	</button>
</div>

{#if isOpen}
	<button
		type="button"
		class="fixed inset-0 z-40 bg-slate-900/20"
		onclick={() => (isOpen = false)}
		aria-label="Close panel overlay"
	></button>
{/if}

<div
	class={`fixed top-0 right-0 z-50 h-screen w-full max-w-md border-l border-slate-200 bg-white/95 shadow-2xl transition-transform duration-300 ease-in-out sm:max-w-xl ${
		isOpen ? 'translate-x-0' : 'translate-x-full'
	}`}
>
	{#if isOpen}
		<div class="flex h-full flex-col">
			<div class="border-b border-slate-200 px-4 py-4 sm:px-5">
				<div class="flex items-center justify-between gap-3">
					<div>
						<h2 class="text-lg font-bold text-slate-900">Trait Explanation Panel</h2>
						<p class="mt-1 text-xs text-slate-500">
							Browse typologies, abuse flavors, vulnerability types, and trauma signs.
						</p>
					</div>

					<button
						type="button"
						class="rounded-full border border-slate-200 bg-white p-2 text-slate-600 transition hover:bg-slate-50"
						onclick={() => (isOpen = false)}
					>
						<X class="h-4 w-4" />
					</button>
				</div>

				<div class="relative mt-4">
					<Search
						class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400"
					/>
					<input
						bind:value={search}
						type="text"
						placeholder="Search categories, traits, red flags, techniques..."
						class="w-full rounded-2xl border border-slate-200 bg-white py-3 pr-4 pl-10 text-sm text-slate-800 outline-none transition focus:border-slate-300"
					/>
				</div>

				<div class="mt-4 flex flex-wrap gap-2">
					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'typologies'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'typologies')}
					>
						Typologies
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'flavors'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'flavors')}
					>
						Flavors
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'vulnerabilities'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'vulnerabilities')}
					>
						Vulnerability
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'trauma'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'trauma')}
					>
						Trauma
					</button>
				</div>
			</div>

			<div class="flex-1 overflow-y-auto px-4 py-4 sm:px-5">
				{#if activeTab === 'typologies'}
					<div class="space-y-3">
						{#each filteredTypologies as item}
							<details class="rounded-2xl border border-slate-200 bg-white p-4">
								<summary class="cursor-pointer list-none">
									<h3 class="text-sm font-semibold text-slate-900">{item.name}</h3>
									{#if item.summary}
										<p class="mt-2 line-clamp-3 text-xs leading-5 text-slate-600">
											{item.summary}
										</p>
									{/if}
								</summary>

								<div class="mt-4 space-y-4 border-t border-slate-100 pt-4">
									{#if cleanList(item.main_motivation, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Main motivation
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.main_motivation, 4) as value}
													<span
														class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}

									{#if cleanList(item.flavors_of_abuse, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Abuse flavors
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.flavors_of_abuse, 4) as value}
													<span
														class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}

									{#if cleanList(item.red_flags, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Red flags
											</p>
											<ul class="space-y-1 text-xs leading-5 text-slate-600">
												{#each cleanList(item.red_flags, 4) as value}
													<li>• {value}</li>
												{/each}
											</ul>
										</div>
									{/if}

									{#if cleanList(item.techniques_he_might_use, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Techniques
											</p>
											<ul class="space-y-1 text-xs leading-5 text-slate-600">
												{#each cleanList(item.techniques_he_might_use, 4) as value}
													<li>• {value}</li>
												{/each}
											</ul>
										</div>
									{/if}

									{#if cleanList(item.trauma_signs, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Trauma signs
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.trauma_signs, 4) as value}
													<span
														class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}
								</div>
							</details>
						{/each}

						{#if filteredTypologies.length === 0}
							<p class="text-sm text-slate-500">No typologies matched your search.</p>
						{/if}
					</div>
				{/if}

				{#if activeTab === 'flavors'}
					<div class="space-y-3">
						{#each filteredFlavors as item}
							<div class="rounded-2xl border border-slate-200 bg-white p-4">
								<h3 class="text-sm font-semibold text-slate-900">{item.Flavor}</h3>
								<div class="mt-3 flex flex-wrap gap-2">
									{#each cleanList(item['Player typologies'], 6) as value}
										<span class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700">
											{value}
										</span>
									{/each}
								</div>
							</div>
						{/each}

						{#if filteredFlavors.length === 0}
							<p class="text-sm text-slate-500">No flavors matched your search.</p>
						{/if}
					</div>
				{/if}

				{#if activeTab === 'vulnerabilities'}
					<div class="space-y-3">
						{#each filteredVulnerabilities as item}
							<details class="rounded-2xl border border-slate-200 bg-white p-4">
								<summary class="cursor-pointer list-none">
									<h3 class="text-sm font-semibold text-slate-900">{item.name}</h3>
								</summary>

								<div class="mt-4 space-y-4 border-t border-slate-100 pt-4">
									{#if cleanList(item.vulnerability_traits, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Vulnerability traits
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.vulnerability_traits, 4) as value}
													<span
														class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}

									{#if cleanList(item.abuse_techniques, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Abuse techniques
											</p>
											<ul class="space-y-1 text-xs leading-5 text-slate-600">
												{#each cleanList(item.abuse_techniques, 4) as value}
													<li>• {value}</li>
												{/each}
											</ul>
										</div>
									{/if}

									{#if cleanList(item.brain_biases, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Brain biases
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.brain_biases, 4) as value}
													<span
														class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}

									{#if cleanList(item.flavors_of_abuse, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Related flavors
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.flavors_of_abuse, 4) as value}
													<span
														class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}

									{#if cleanList(item.player_typologies, 4).length}
										<div>
											<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
												Related typologies
											</p>
											<div class="flex flex-wrap gap-2">
												{#each cleanList(item.player_typologies, 4) as value}
													<span
														class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
													>
														{value}
													</span>
												{/each}
											</div>
										</div>
									{/if}
								</div>
							</details>
						{/each}

						{#if filteredVulnerabilities.length === 0}
							<p class="text-sm text-slate-500">No vulnerability types matched your search.</p>
						{/if}
					</div>
				{/if}

				{#if activeTab === 'trauma'}
					<div class="space-y-3">
						{#each filteredTrauma as item}
							<div class="rounded-2xl border border-slate-200 bg-white p-4">
								<h3 class="text-sm font-semibold text-slate-900">{item.Name}</h3>

								{#if item['Research Summary']}
									<p class="mt-2 text-xs leading-5 text-slate-600">{item['Research Summary']}</p>
								{/if}

								{#if cleanList(item['Player Typologies'], 4).length}
									<div class="mt-3">
										<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
											Related typologies
										</p>
										<div class="flex flex-wrap gap-2">
											{#each cleanList(item['Player Typologies'], 4) as value}
												<span
													class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{value}
												</span>
											{/each}
										</div>
									</div>
								{/if}

								{#if cleanList(item['Abuse Techniques'], 4).length}
									<div class="mt-3">
										<p class="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
											Related techniques
										</p>
										<ul class="space-y-1 text-xs leading-5 text-slate-600">
											{#each cleanList(item['Abuse Techniques'], 4) as value}
												<li>• {value}</li>
											{/each}
										</ul>
									</div>
								{/if}
							</div>
						{/each}

						{#if filteredTrauma.length === 0}
							<p class="text-sm text-slate-500">No trauma items matched your search.</p>
						{/if}
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>