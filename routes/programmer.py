from flask import Flask, request, jsonify
from collections import defaultdict
import sys
import json

import logging

from flask import request

from routes import app



@app.route('/the-clumsy-programmer', methods=['POST'])
def the_clumsy_programmer():
    try:
        # Parse JSON input
        data = request.get_json()
        if not data or not isinstance(data, list) or len(data) == 0:
            return jsonify({"error": "Invalid input format"}), 400
        
        input_obj = data[0]
        dictionary = input_obj.get("dictionary", [])
        mistypes = input_obj.get("mistypes", [])
        
        # Check if dictionary and mistypes are lists
        if not isinstance(dictionary, list) or not isinstance(mistypes, list):
            return jsonify({"error": "Dictionary and mistypes should be lists"}), 400
        
        if not dictionary:
            return jsonify({"error": "Dictionary is empty"}), 400
        
        L = len(dictionary[0])
        # Verify all dictionary words have the same length
        for word in dictionary:
            if len(word) != L:
                return jsonify({"error": "All dictionary words must have the same length"}), 400
        
        # Build mask_to_word mapping
        mask_to_word = {}
        for word in dictionary:
            for i in range(L):
                mask = word[:i] + '*' + word[i+1:]
                if mask in mask_to_word:
                    # If multiple words share the same mask, mark as ambiguous
                    mask_to_word[mask] = None
                else:
                    mask_to_word[mask] = word
        
        corrections = []
        for mistyped in mistypes:
            if len(mistyped) != L:
                return jsonify({"error": f"Mistyped word '{mistyped}' does not match required length {L}"}), 400
            found = None
            for i in range(L):
                mask = mistyped[:i] + '*' + mistyped[i+1:]
                candidate = mask_to_word.get(mask)
                if candidate:
                    found = candidate
                    break
            if found:
                corrections.append(found)
            else:
                # If no correction found, append an empty string or handle as needed
                corrections.append("")
        
        return jsonify([{"corrections": corrections}]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

