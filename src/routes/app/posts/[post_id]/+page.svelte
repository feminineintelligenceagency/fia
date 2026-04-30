<script lang="ts">
	import ScrollText from '@lucide/svelte/icons/scroll-text';
	import Markdown from 'svelte-exmarkdown';

	let { data } = $props();
</script>

<div class="relative mx-auto w-full max-w-7xl px-4 py-6">
	<div class="mb-8 flex items-center justify-between">
		<div class="flex items-center gap-4">
			<div
				class="flex h-12 w-12 items-center justify-center rounded-xl bg-linear-to-br from-pink-500 to-purple-600 shadow-lg shadow-pink-500/25"
			>
				<ScrollText class="h-6 w-6 text-white" />
			</div>
			<div>
				<h1
					class="bg-linear-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-3xl font-bold text-transparent"
				>
					Analysis Summary
				</h1>
				<p class="text-sm text-muted-foreground">AI-detected patterns from analyzed scripts</p>
			</div>
		</div>
	</div>

	<div class="w-full">
		<h1 class="scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
			{data.post.title}
		</h1>
		<article class="mx-auto prose mt-6 w-full dark:prose-invert">
			<Markdown md={data.post.body} />
		</article>
	</div>
</div>
