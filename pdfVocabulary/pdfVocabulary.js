const fs = require('fs');
const pdf = require('pdf-parse');
const stopword = require('stopword');

// Function to extract text from PDF
async function extractTextFromPDF(filePath) {
  const dataBuffer = fs.readFileSync(filePath);
  const data = await pdf(dataBuffer);
  return data.text;
}

// Function to replace non-breaking hyphens with regular hyphens
function replaceNonBreakingHyphens(text) {
  return text.replace(/\u2011/gmu, '-');
}

// Function to get unique words from text
function getUniqueWords(text) {
  // Remove punctuation except hyphens and non-breaking hyphens, convert to lower case, and split into words
  // const words = text.replace(/[^\p{L}\p{N}\s-]/gu, '').toLowerCase().split(/\s+/);
  const words = text.replace(/[^\p{L}\p{N}\s’\-\u2011]/gu, ' ').toLowerCase().split(/\s+/);
  // Remove stopwords
  const filteredWords = stopword.removeStopwords(words);
  // Get unique words
  const uniqueWords = [...new Set(filteredWords)];

  return uniqueWords.sort();
}

// Function to save unique words to a text file
function saveWordsToFile(words, outputPath) {
  const fileContent = words.join('\n');
  fs.writeFileSync(outputPath, fileContent, 'utf8');
}

// Main function
async function main() {
  const pdfPath = './antoloġija-1-test.pdf'; // Replace with your PDF file path
  const outputPath = 'unique_words.txt'; // Output file path
  const text = await extractTextFromPDF(pdfPath);
  const textWithHyphens = replaceNonBreakingHyphens(text);
  const uniqueWords = getUniqueWords(textWithHyphens);
  saveWordsToFile(Array.from(uniqueWords).sort((a, b) => b.length - a.length), outputPath);
  console.log(`Unique words have been saved to ${outputPath}`);
}

main().catch((err) => {
  console.error('Error:', err);
});
