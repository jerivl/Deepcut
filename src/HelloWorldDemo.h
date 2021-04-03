/*
  ==============================================================================

   This file is part of the JUCE examples.
   Copyright (c) 2020 - Raw Material Software Limited

   The code included in this file is provided under the terms of the ISC license
   http://www.isc.org/downloads/software-support-policy/isc-license. Permission
   To use, copy, modify, and/or distribute this software for any purpose with or
   without fee is hereby granted provided that the above copyright notice and
   this permission notice appear in all copies.

   THE SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY, AND ALL WARRANTIES,
   WHETHER EXPRESSED OR IMPLIED, INCLUDING MERCHANTABILITY AND FITNESS FOR
   PURPOSE, ARE DISCLAIMED.

  ==============================================================================
*/

/*******************************************************************************
 The block below describes the properties of this PIP. A PIP is a short snippet
 of code that can be read by the Projucer and used to generate a JUCE project.

 BEGIN_JUCE_PIP_METADATA

 name:             HelloWorldDemo
 version:          1.0.0
 vendor:           JUCE
 website:          http://juce.com
 description:      Simple HelloWorld application.

 dependencies:     juce_core, juce_data_structures, juce_events, juce_graphics,
                   juce_gui_basics
 exporters:        xcode_mac, vs2019, linux_make, xcode_iphone

 moduleFlags:      JUCE_STRICT_REFCOUNTEDPOINTER=1

 type:             Component
 mainClass:        HelloWorldDemo

 useLocalCopy:     1

 END_JUCE_PIP_METADATA

*******************************************************************************/

#pragma once


//==============================================================================
class HelloWorldDemo  : public Component
{
public:
    //==============================================================================
    HelloWorldDemo()
    {
		//Welcome message
        addAndMakeVisible (WelcomeMessage);
        WelcomeMessage.setFont (Font (20.00f, Font::bold));
        WelcomeMessage.setJustificationType (Justification::centredTop);
        WelcomeMessage.setEditable (false, false, false);
        WelcomeMessage.setColour (Label::textColourId, Colours::black);
        WelcomeMessage.setColour (TextEditor::textColourId, Colours::white);
        WelcomeMessage.setColour (TextEditor::backgroundColourId, Colour (0x00000000));

		//Instructions
		addAndMakeVisible(instructionText);
		instructionText.setText("Type in text in the box below", dontSendNotification);
		instructionText.setFont(Font(15.00f, Font::bold));
		instructionText.setJustificationType(Justification::centredTop);
		instructionText.setColour(Label::textColourId, Colours::black);

		//Label that says "Input text here"
		addAndMakeVisible(inputLabel);
		inputLabel.setText("Input text here: ", dontSendNotification);
		inputLabel.attachToComponent(&inputText, true);
		inputLabel.setFont(Font(15.00f, Font::bold));
		inputLabel.setJustificationType(Justification::left);
		inputLabel.setColour(Label::textColourId, Colours::black);

		//Text box to input text
		//Colour of the text is white. Figure out how to change it to black
		addAndMakeVisible(inputText);
		inputText.setEditable(true);
		inputText.setColour(Label::textColourId, Colours::black);
		inputText.setColour(Label::textWhenEditingColourId, Colours::black);
		inputText.setColour(Label::backgroundColourId, Colours::white);
		inputText.setColour(Label::outlineColourId, Colours::black);
		inputText.onTextChange = [this] { outputText.setText(inputText.getText(), juce::dontSendNotification); };

		//Output label for the text
		addAndMakeVisible(outputLabel);
		outputLabel.setText("Output Text: ", dontSendNotification);
		outputLabel.attachToComponent(&outputText, true);
		outputLabel.setFont(Font(15.00f, Font::bold));
		outputLabel.setJustificationType(Justification::left);
		outputLabel.setColour(Label::textColourId, Colours::black);

		//Outputs the text that was typed into the text box
		addAndMakeVisible(outputText);
		outputText.setColour(Label::outlineColourId, Colours::black);
		outputText.setColour(Label::backgroundColourId, Colours::white);
		outputText.setColour(Label::textColourId, Colours::black);
		
		addAndMakeVisible (quitButton);
        quitButton.onClick = [] { JUCEApplication::quit(); };

        setSize (600, 300);
    }

    //==============================================================================
    void paint (Graphics& g) override
    {
        //g.fillAll (Colour (0xffc1d0ff));
		g.fillAll(Colour(0xffffffff));

        g.setColour (Colours::white);
        g.fillPath (internalPath);

        g.setColour (Colour (0xff6f6f6f));
        g.strokePath (internalPath, PathStrokeType (5.200f));
    }

    void resized() override
    {
        WelcomeMessage.setBounds (10, 10, getWidth() - 20, 30);
		instructionText.setBounds(10, 30, getWidth() - 20, 30);
		inputText.setBounds(110, 50, getWidth() - 110, 20);
		outputText.setBounds(110, 80, getWidth() - 110, 20);
        quitButton.setBounds (getWidth() - 176, getHeight() - 60, 120, 32);

        internalPath.clear();
        internalPath.startNewSubPath (136.0f, 80.0f);
        internalPath.closeSubPath();
    }

private:
    //==============================================================================
    Label WelcomeMessage { {}, TRANS("Welcome!") };
	Label instructionText;
	Label inputLabel;
	Label inputText;
	Label outputLabel;
	Label outputText;
    TextButton quitButton { TRANS("Quit") };
    Path internalPath;

    //==============================================================================
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (HelloWorldDemo)
};
