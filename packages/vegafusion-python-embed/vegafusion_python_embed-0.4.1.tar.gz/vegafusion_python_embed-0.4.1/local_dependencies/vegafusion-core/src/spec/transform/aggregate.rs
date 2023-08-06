/*
 * VegaFusion
 * Copyright (C) 2022 VegaFusion Technologies LLC
 *
 * This program is distributed under multiple licenses.
 * Please consult the license documentation provided alongside
 * this program the details of the active license.
 */
use crate::spec::transform::TransformSpecTrait;
use crate::spec::values::Field;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AggregateTransformSpec {
    pub groupby: Vec<Field>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub fields: Option<Vec<Option<Field>>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub ops: Option<Vec<AggregateOpSpec>>,

    #[serde(rename = "as", skip_serializing_if = "Option::is_none")]
    pub as_: Option<Vec<Option<String>>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub cross: Option<bool>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub drop: Option<bool>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub key: Option<Field>,

    #[serde(flatten)]
    pub extra: HashMap<String, Value>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, Hash)]
#[serde(rename_all = "lowercase")]
pub enum AggregateOpSpec {
    Count,
    Valid,
    Missing,
    Distinct,
    Sum,
    Product,
    Mean,
    Average,
    Variance,
    Variancep,
    Stdev,
    Stdevp,
    Stderr,
    Median,
    Q1,
    Q3,
    Ci0,
    Ci1,
    Min,
    Max,
    Argmin,
    Argmax,
    Values,
}

impl AggregateOpSpec {
    pub fn name(&self) -> String {
        serde_json::to_value(self)
            .unwrap()
            .as_str()
            .unwrap()
            .to_string()
    }
}

impl TransformSpecTrait for AggregateTransformSpec {
    fn supported(&self) -> bool {
        // Check for supported aggregation op
        use AggregateOpSpec::*;
        let ops = self.ops.clone().unwrap_or_else(|| vec![Count]);
        for op in &ops {
            if !matches!(
                op,
                Count
                    | Valid
                    | Missing
                    | Distinct
                    | Sum
                    | Mean
                    | Average
                    | Min
                    | Max
                    | Variance
                    | Variancep
                    | Stdev
                    | Stdevp
            ) {
                // Unsupported aggregation op
                return false;
            }
        }

        // Cross aggregation not supported
        if let Some(true) = &self.cross {
            return false;
        }

        // drop=false not support
        if let Some(false) = &self.drop {
            return false;
        }
        true
    }
}
