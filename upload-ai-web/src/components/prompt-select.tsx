import { useEffect, useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { api } from "@/lib/axios";

interface Prompt {
    id: string,
    title: string,
    template: string
}

interface PrompSelectProps {
    onPromptSelected: (template: string) => void
}

export function PromptSelect(props: PrompSelectProps) {
    const [prompts, setPrompts] = useState<Prompt[] | null>(null);

    useEffect(() => {
        api.get("/prompts").then(response => {
            setPrompts(response.data.data)
        })
    }, [])

    function handlePromptSelected(promptId: string) {
        const selectedPrompt = prompts?.find(prompt => prompt.id == promptId);

        if (!selectedPrompt) {
            return
        }

        props.onPromptSelected(selectedPrompt.template)
    }

    return (
        <Select onValueChange={handlePromptSelected}>
            <SelectTrigger>
                <SelectValue placeholder="Selecione um prompt"></SelectValue>
            </SelectTrigger>
            <SelectContent>
                {prompts?.map(e => {
                    return (
                        <SelectItem key={e.id} value={e.id}>
                            {e.title}
                        </SelectItem>
                    )
                })}
            </SelectContent>
        </Select>
    )
}