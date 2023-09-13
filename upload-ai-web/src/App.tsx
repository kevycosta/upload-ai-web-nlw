import { Button } from "./components/ui/button";
import {FileVideo, Github, Upload, Wand2 } from "lucide-react";
import { Separator } from "./components/ui/separator";
import { Textarea } from "./components/ui/textarea";
import { Label } from "./components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Slider } from "./components/ui/slider";

export function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <div className="px-6 py-3 flex items-center justify-between border-b" >
        <h1 className="text-xl font-bold">upload.ai</h1>

        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground">Estudando React no NLW AI da RocketSeat</span>

          <Separator orientation="vertical" className="h-6"></Separator>

          <Button variant={"outline"}>
            <Github className="w-4 h-4 mr-2"></Github>
            Github
          </Button>
        </div>
      </div>

      <main className="flex-1 p-6 flex gap-6">
        <div className="flex flex-col flex-1 gap-4">
          <div className="grid grid-rows-2 gap-4 flex-1">
            <Textarea 
              className="resize-none p-4 leading-relaxed"
              placeholder="Inclua o prompt para a IA."
            ></Textarea>
            <Textarea 
              className="resize-none p-4 leading-relaxed"
              placeholder="Resultado gerado para IA" 
              readOnly
            ></Textarea>
          </div>

          <p className="text-sm text-muted-foreground">
            Lembre-se: você pode usar a variável <code className="text-primary/50">{'{transcription}'}</code> no seu prompt para adicionar o conteúdo da transcrição do video selecionado.
          </p>
        </div>

        <aside className="w-80 space-y-6">
          <form className="space-y-6">
            <label 
              htmlFor="video" 
              className="border flex rounded-md aspect-video cursor-pointer border-dashed text-sm flex-col gap-2 justify-center items-center text-muted-foreground hover:bg-primary/5"
            >
              <FileVideo></FileVideo>
              Selecione um vídeo.
            </label>

            <input type="file" id="video" accept="video/mp4" className="sr-only"/>

            <Separator className=""></Separator>
            
            <div className="space-y-2">
              <Label htmlFor="transcription_prompt">Prompt de transcrição</Label>
              <Textarea 
                id="transcription_prompt" 
                className="h-20 leading-relaxed resize-none" 
                placeholder="Inclua palavras-chave mecionadas no vídeo separadas por (,)"
              ></Textarea>
            </div>

            <Button type="submit" className="w-full">
              Carregar Video
              <Upload className="w-4 h-4 ml-2"></Upload>
            </Button>
          </form>

          <Separator></Separator>

          <form className="space-y-6">
            <div className="space-y-2">
              <Label>Prompt</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um prompt"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="title">Titulo do Youtube</SelectItem>
                  <SelectItem value="description">Descrição do Youtube</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Modelo</Label>
              <Select disabled defaultValue="gpt3.5">
                <SelectTrigger>
                  <SelectValue></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt3.5">GPT 3.5-turbo 16k</SelectItem>
                </SelectContent>
              </Select>
              <span className="block text-xs text-muted-foreground italic">
                Você poderá customizar essa opção em breve
              </span>
            </div>

            <Separator></Separator>

            <div className="space-y-4">
              <Label>Temperatura</Label>
              <Slider 
                min={0} 
                max={1}
                step={0.1}
              ></Slider>
              <span className="block text-xs text-muted-foreground leading-relaxed">
                Valores mais altos tendem a deixar o resultado mais criativo e com possiveis erros
              </span>
            </div>

            <Separator></Separator>

            <Button type="submit" className="w-full">
              Executar
              <Wand2 className="w-4 h-4 ml-2"></Wand2>
            </Button>

          </form>

        </aside>
      </main>
    </div>
  )
}
