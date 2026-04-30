<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { handleError } from '$lib/consts';
	import { analyzeUploadedScript } from '$lib/data.remote';
	import { toast } from 'svelte-sonner';

	let btnDisabled = $state(false);
	let done = $state(false);
</script>

<div class="flex h-full flex-col">
	<div class="flex-1 overflow-y-auto p-6">
		<article class="mx-auto prose max-w-5xl dark:prose-invert">
			{#if done}
				<p>Analysis complete.</p>
			{:else if btnDisabled}
				<p>Analyzing...</p>
			{:else}
				<p>Upload a script file to get started.</p>
			{/if}
		</article>
	</div>

	<div class="sticky bottom-0 rounded-lg border bg-background/80 p-4 backdrop-blur-md">
		<form
			enctype="multipart/form-data"
			{...analyzeUploadedScript.enhance(async ({ submit }) => {
				btnDisabled = true;
				try {
					toast.promise(submit, {
						loading: 'Analyzing script...',
						success: 'Analysis complete',
						error: 'Analysis failed'
					});
					await submit;
					done = true;
				} catch (err) {
					handleError(err);
				} finally {
					btnDisabled = false;
				}
			})}
			class="flex gap-2"
		>
			<Input type="file" name="file" accept=".txt" disabled={btnDisabled} class="flex-1" />
			<Button type="submit" class="mt-auto" size="sm" disabled={btnDisabled}>Analyze</Button>
		</form>
	</div>
</div>
