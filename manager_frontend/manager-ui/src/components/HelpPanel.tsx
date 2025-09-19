// src/components/HelpPanel.tsx
import React from "react"
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion"

const HelpPanel: React.FC = () => {
  return (
    <section className="h-full flex flex-col bg-background text-foreground">
      <h2 className="font-bold mb-4 text-lg">Info</h2>

      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="what-to-do">
          <AccordionTrigger className="bg-background text-foreground">
            What to do?
          </AccordionTrigger>
          <AccordionContent className="bg-background text-foreground">
            Select one or more goals and click <b>Fetch</b> to generate proposals.
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="under-the-hood">
          <AccordionTrigger className="bg-background text-foreground">
            What is happening under the hood?
          </AccordionTrigger>
          <AccordionContent className="bg-background text-foreground">
            Agents generate strategies using product & customer data. Proposals
            are stored in Redis and shown here.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  )
}

export default HelpPanel
